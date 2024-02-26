
class Calculator:

    units_of_mesurement = {
        'velocity': 'meters/second',
        'acceleration': 'meters/second^2',
        'time': 'seconds',
        'distance': 'meters',
        'mass': 'kg',
        'motor_force': 'newton',
    }

    def __init__(self, V0: float = 0, X0: float = 0):
        self.V0 = V0
        self.X0 = X0

    @staticmethod
    def acceleration(F: int, m: float) -> float:
        """
        calculates acceleration based on the FMA equation

        :param F: Force (newtons)
        :param m: Mass (kg)

        :return: acceleration in meters/second^2
        """
        return F / m

    def time(self, V: float, a: float) -> float:
        """
        calculates time based on the Velocity-Time Equation

        :param V: velocity (meters/seconds)
        :param a: acceleration (meters/seconds^2)

        :return: time in seconds
        """
        return (V - self.V0) / a

    def distance(self, a: float, t: float) -> float:
        """
        calculates travel distance based on the Displacement-Time Equation

        :param a: acceleration (meters/seconds^2)
        :param t: time (seconds)

        :return: distance in meters
        """
        return 0.5 * a * pow(t, 2) + self.V0 * t + self.X0

    @staticmethod
    def extra_mass(t: float, am: float, pm: float, V: float, F: int) -> float:
        """
        calculates the max amount of mass allowed given the parameters

        :param t: time (seconds)
        :param am: aircraft mass (kg)
        :param pm: payload mass (kg)
        :param V: velocity (meters/second)
        :param F: force (newtons)

        :return: extra mass in kg (rounded by 3 decimel numbers)
        """
        accel = V / 60
        excess_payload_mass = ((F - accel * am) / accel)
        extra_mass = pm - excess_payload_mass

        return extra_mass
