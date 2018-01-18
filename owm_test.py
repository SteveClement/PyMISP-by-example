#!/usr/bin/env python3
# -*- coding: utf-8 -*-

print("This test script will make sure you have: \n - Internetz \n - A valid configuration file config/keys.py \n - The ability to get weather data for the current location\n\n\n")

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

# To search for current weather in London (Great Britain): London,GB

currLoc = j['country_name'] + ',' + j['country_code']

try:
    if forceLoc: currLoc = forceLoc
    observation = owm.weather_at_place(currLoc)
except pyowm.exceptions.unauthorized_error.UnauthorizedError as e:
    print(f"Something went wrong:\n {e}")
    sys.exit(6)

w = observation.get_weather() # Type: pyowm.webapi25.weather.Weather - Docu: https://pyowm.readthedocs.io/en/latest/pyowm.webapi25.html

if w.get_rain():
    print("Current rain info: {}".format(w.get_rain()))
if w.get_snow():
    print("Current snow info: {}".format(w.get_snow()))

# Weather details
print(f"Weather details for {currLoc} - Test script\n\n\n")
print("Current wind speed in km/h: {}".format(w.get_wind()['speed']*3.6)) # {'speed': 4.6, 'deg': 330}
print("Current temperatur in degC: {}".format(w.get_temperature('celsius')['temp']))  # {'temp_max': 10.5, 'temp': 9.7, 'temp_min': 9.0}

if DEBUG:
    # Search current weather observations in the surroundings of
    # lat=22.57W, lon=43.12S (Rio de Janeiro, BR)
    observation_list = owm.weather_around_coords(-22.57, -43.12)
    print("####### ---> DEBUG OUTPUT <--- #######")
    print(observation_list)
    print("\n\n\n")
    if j['city']:
        print(j['city'].encode('iso-8859-1').decode())
        print("\n\n\n")
    print(f"Humidity for {currLoc}: {w.get_humidity()}")              # 87
    print(f"Weather for {currLoc}: \n {w}") # <Weather - reference time=2013-12-18 09:20, status=Clouds>

print(f"Actual JSON of our weather object: \n{w.to_JSON()}")
