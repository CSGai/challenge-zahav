from fastapi import APIRouter, Request, HTTPException
from src.services.physics_calculator.physics_calc import Calculator
from src.services.sql.sql_wrapper import SQLmanager

router = APIRouter()

known_prop = {
    'velocity': {'value': 140, 'unit': 'meters/second'},
    'motor_force': {'value': 100000, 'unit': 'newton'},
    'mass': {'value': 35000, 'unit': 'kg'}
}

# initialize
sql = SQLmanager('zahav.db')
calc = Calculator()
units = calc.units_of_mesurement


@router.post("/Calculator")
async def time_and_distance(request: Request):

    try:
        # get request data
        data = await request.json()
        payload_mass = data.get('mass')

        # handle edge cases
        if payload_mass is None:
            raise HTTPException(status_code=400, detail="Payload Mass is Missing")

        if not isinstance(payload_mass, (int, float)):
            raise HTTPException(status_code=400, detail="Payload Mass Must be a Number")

        payload_mass = float(payload_mass)

        if payload_mass <= 0:
            raise HTTPException(status_code=400, detail="Payload Mass Cannot Be Negative")

        # extract aircraft known properties
        aircraft_mass = known_prop['mass']['value']
        velocity = known_prop['velocity']['value']
        force = known_prop['motor_force']['value']

        # main calculation
        total_mass = payload_mass + aircraft_mass

        accel = calc.acceleration(F=force, m=total_mass)
        time = calc.time(V=velocity, a=accel)
        takeoff_distance = calc.distance(a=accel, t=time)

        if time <= 60:

            time = round(time, 3)
            takeoff_distance = round(takeoff_distance, 3)

            # insert data to sql database
            insert_data = {
                'payload_mass': payload_mass,
                'takeoff_distance': takeoff_distance,
                'excess_payload_mass': 0,
                'takeoff_time': time
            }
            sql.insert_row('calc_results', insert_data)

            # return final results
            return {
                'takeoff_distance': {'value': takeoff_distance, 'unit': units['distance']},
                'takeoff_time': {'value': time, 'unit': units['time']}
            }

        else:

            excess_mass = round(calc.extra_mass(t=time, am=aircraft_mass, pm=payload_mass, V=velocity, F=force), 3)

            # insert data to sql database
            insert_data = {
                'payload_mass': payload_mass,
                'takeoff_distance': takeoff_distance,
                'excess_payload_mass': excess_mass,
                'takeoff_time': time
            }
            sql.insert_row('calc_results', insert_data)

            # return final results
            return {'extra_weight': excess_mass, 'unit': units['mass']}

    # handle unexpected internal exceptions
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
