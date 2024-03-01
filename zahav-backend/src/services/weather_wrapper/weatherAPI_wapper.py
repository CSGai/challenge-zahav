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

    async def get_weather(self) -> dict:
        """
        gets the weather in the set coordinates and date

        :return: info from the weather api
        """

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

        print(url)

        # write data handling logic for the 3 instances.

        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            return response.json()

    @staticmethod
    async def process_date(date: str):
        """
        converts date as string to a date object
        :param date:
        :return: date object
        """
        return datetime.strptime(date, '%Y-%m-%d')


async def test_runner():
    weather = WeatherAPI((30, 35))
    await weather.set_datetime(datetime(2023, 1, 1, 15, 11, 0))
    res = json.dumps(await weather.get_weather(), indent=2)
    print(res)


asyncio.run(test_runner())
