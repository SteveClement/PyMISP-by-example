#!/usr/bin/env python3

try:
    from config.keys import *
except ImportError:
    print("Please make sure you have a valid config file in config/keys.py")

import pyowm
import requests
import json
import sys

try:
    r = requests.get(freeGeoIP_url)
    j = json.loads(r.text)
except requests.exceptions.ConnectionError as e:
    print(f"Some form of ConnectionError exception has occured: \n {e}")
    sys.exit(4)

owm = pyowm.OWM(owm_key)  # You MUST provide a valid API key

# Have a pro subscription? Then use:
# owm = pyowm.OWM(API_key='your-API-key', subscription_type='pro')

# Search for current weather in London (Great Britain)
try:
    observation = owm.weather_at_place('London,GB')
except pyowm.exceptions.unauthorized_error.UnauthorizedError as e:
    print(f"Something went wrong:\n {e}")
    sys.exit(6)

w = observation.get_weather()
print(w)                      # <Weather - reference time=2013-12-18 09:20,
                              # status=Clouds>

# Weather details
w.get_wind()                  # {'speed': 4.6, 'deg': 330}
w.get_humidity()              # 87
w.get_temperature('celsius')  # {'temp_max': 10.5, 'temp': 9.7, 'temp_min': 9.0}

# Search current weather observations in the surroundings of
# lat=22.57W, lon=43.12S (Rio de Janeiro, BR)
observation_list = owm.weather_around_coords(-22.57, -43.12)
