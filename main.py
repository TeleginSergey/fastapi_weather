"""Module that takes weather on next part of day."""
import json
from datetime import datetime

import requests

from fastapi import FastAPI

app = FastAPI()

YANDEX_KEY = '5a8a7ae8-29fe-43f1-900d-320d6f7d51e8'
URL = 'https://api.weather.yandex.ru/v2/forecast?lat=43.413249&lon=39.949388'
OK = 200

DAY_TIME_START = 6
MORNING_TIME_START = 0
NIGHT_TIME_START = 18
EVENING_TIME_START = 12


class ForeignApiError(Exception):
    """
    Exception raised for errors in the foreign API.

    Attributes:
        api_name: Name of the API.
        status_code: Status code returned by the API.
    """

    def __init__(self, api_name: str, status_code: int):
        """
        Initialize the ForeignApiError exception.

        Args:
            api_name: Name of the API.
            status_code: Status code returned by the API.
        """
        super().__init__(f'Request to API {api_name} ended with {status_code}')


@app.get('/weather_next')
def get_weather(lat: float, lon: float):
    """
    Get the weather forecast based on latitude and longitude.

    Args:
        lat: Latitude coordinate.
        lon: Longitude coordinate.

    Returns:
        dict: Weather forecast for the specified coordinates.
    """
    coordinates = {'lat': lat, 'lon': lon}
    response = requests.get(
        URL, headers={'X-Yandex-API-Key': YANDEX_KEY}, params=coordinates,
        )

    if response.status_code != OK:
        return ForeignApiError('Yandex.Weather', response.status_code)

    current_time = datetime.now()
    part_day = ''

    if current_time in list(range(MORNING_TIME_START, DAY_TIME_START)):
        part_day = 'morning'
    elif current_time in list(range(DAY_TIME_START, EVENING_TIME_START)):
        part_day = 'day'
    elif current_time in list(range(EVENING_TIME_START, NIGHT_TIME_START)):
        part_day = 'evening'
    else:
        part_day = 'night'

    return json.loads(response.content)['forecasts'][0]['parts'][part_day]
