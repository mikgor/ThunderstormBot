import json
import requests
from TSB.local_settings import *

class WeatherApiHandler:
    def Request(self, params):
        r = requests.get("http://api.openweathermap.org/data/2.5/find?cnt=50&"+params+"&APPID="+WEATHER_API_KEY)
        return r.json()
