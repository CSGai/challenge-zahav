from datetime import datetime
import httpx

# test module imports
import asyncio
import json


class WeatherAPI:
    """
    this api wrapper was meant to work both with dates and datetime
    """

    url_templates = [
        # future
        "https://api.open-meteo.com/v1/forecast?latitude={}&longitude={}&forecast_days={}&hourly=temperature_2m",
        # past
        "https://archive-api.open-meteo.com/v1/era5?latitude={}&longitude={}"
        "&start_date={}&end_date={}&hourly=temperature_2m",
        # current
        "https://api.open-meteo.com/v1/forecast?latitude={}&longitude={}&forecast_days=1&hourly=temperature_2m"
    ]

    def __init__(self, coordinates: tuple):
        """
        initialize the class
        :param coordinates:
        """
        self.date_time = None
        self.latitude, self.longitude = coordinates

    async def set_datetime(self, new_date_time: any):
        """
        sets the current datetime of the instance
        :param new_date_time:
        :return: None
        """
        self.date_time = new_date_time

    async def set_coordinates(self, new_coordinates: tuple):
        """
        sets the current instance's coordinates
        :param new_coordinates:
        :return: None
        """
        self.longitude, self.latitude = new_coordinates

    async def approved_takeoff_hours(self, temper_limits: tuple):
        """
        gets the weather in the set coordinates and date
        :param temper_limits: a tuple containing the min and max temperatures for an approved takeoff
        :return: when the aircraft can take off
        """
        min_temp, max_temp = temper_limits

        focus_date = self.date_time.date()
        cur_date = datetime.now().date()

        # future
        if focus_date > cur_date:
            delta = (focus_date - cur_date).days + 2
            url = self.url_templates[0].format(self.latitude, self.longitude, delta)

        # past
        elif focus_date != cur_date:
            url = self.url_templates[1].format(self.latitude, self.longitude, focus_date, focus_date)

        # current
        else:
            url = self.url_templates[2].format(self.latitude, self.longitude)

        async with httpx.AsyncClient() as client:
            try:
                takeoff_hours = []
                response = await client.get(url)

                # hourly: {time: list, temperature_2m: list}
                res = response.json()['hourly']
                temper_list = res['temperature_2m']
                datetime_list = res['time']
                date_list = [(await self.process_date(date[:date.find('T')])).date() for date in datetime_list]
                time_list = [time[time.find('T') + 1:] for time in datetime_list]

                for index in range(len(date_list)):
                    if date_list[index] == focus_date:
                        if max_temp > temper_list[index] > min_temp:
                            takeoff_hours.append(time_list[index])

                return takeoff_hours

            except Exception as e:
                print('error:', e)
                return None

    @staticmethod
    async def process_date(date: str):
        """
        converts date as string to a datetime object
        :param date:
        :return: date object
        """
        return datetime.strptime(date, '%Y-%m-%d')


# async def test_runner():
#     weather = WeatherAPI((30, 35))
#     await weather.set_datetime(datetime(2015, 12, 5, 15, 11, 0))
#     print(await weather.approved_takeoff_hours((15, 35)))
#
# asyncio.run(test_runner())
