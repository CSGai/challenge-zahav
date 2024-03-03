import json

from fastapi import APIRouter, Request, HTTPException

from src.services.physics_calculator.physics_calc import Calculator

from src.services.sql.sql_wrapper import SQLmanager
from src.services.weather_wrapper.weatherAPI_wapper import WeatherAPI


# init params
db = 'zahav.db'
coords = (30, 35)
known_prop = {
    'velocity': {'value': 140, 'unit': 'meters/second'},
    'motor_force': {'value': 100000, 'unit': 'newton'},
    'mass': {'value': 35000, 'unit': 'kg'}
}


# initialize
weather = WeatherAPI(coords)
sql = SQLmanager(db)
router = APIRouter()
calc = Calculator()

units = calc.units_of_mesurement


@router.post("/api/weather")
async def flight_weather(request: Request):
    try:
        # get request data
        data = await request.json()
        date = await weather.process_date(data['date'])

        await weather.set_datetime(date)
        weather_state = weather.approved_takeoff_hours((15, 35))

        res = await weather_state
        if res:
            return res
        else:
            raise 'you may not take off in the chosen date due to the weather'

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/api/calculator")
async def time_and_distance(request: Request):

    try:
        # get request data
        data = await request.json()
        payload_mass = data.get('mass')

        # handle edge cases
        if payload_mass is None:
            raise HTTPException(status_code=400, detail="Payload Mass is Missing")

        if payload_mass <= 0:
            raise HTTPException(status_code=400, detail="Payload Mass Cannot Be 0 or Negative")

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
                'sub60': 1,
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
            return {'value': excess_mass, 'unit': units['mass']}

    # handle unexpected internal exceptions
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

