#!/usr/bin/env python

import sys
import math
import json
import requests
from datetime import datetime, timezone, date
from astral   import LocationInfo
from astral.sun import sun

city = LocationInfo("New York")
sun  = sun(city.observer, date = date.today())
now  = datetime.now(timezone.utc)
is_night = sun['sunrise'] > now or now > sun['sunset']

WEATHER_CODES = {
    '113': '' , #滛', #☀️',
    '116': ' ', # 杖 #⛅️',
    '119': '摒', #☁️',
    '122': ' ', # 摒', #☁️',
    '143': '' , # 敖', #🌫',
    '176': '' , #🌦',
    '179': '殺', #🌧',
    '182': '殺', #🌧',
    '185': '殺', #🌧',
    '200': '朗', #⛈',
    '227': '殺', #🌨',
    '230': '',  #❄️',
    '248': ' ', #🌫',
    '260': '敖', #🌫',
    '263': '',  #🌦',
    '266': '',  #🌦',
    '281': '殺', #🌧',
    '284': '殺', #🌧',
    '293': '',  #🌦',
    '296': '殺', #🌦',
    '299': '殺', #🌧',
    '302': '殺', #🌧',
    '305': '殺', #🌧',
    '308': '殺', #🌧',
    '311': '殺', #🌧',
    '314': '殺', #🌧',
    '317': '殺', #🌧',
    '320': '殺', #🌨',
    '323': '殺', #🌨',
    '326': '殺', #🌨',
    '329': '',  #❄️',
    '332': '',  # ',  #❄️',
    '335': '',  #❄️',
    '338': '',  #❄️',
    '350': '殺', #🌧',
    '353': '',  #🌦',
    '356': '', #🌧',
    '359': '殺', #🌧',
    '362': '殺', #🌧',
    '365': '殺', #🌧',
    '368': '殺', #🌨',
    '371': '',  #❄️',
    '374': '殺', #🌧',
    '377': '殺', #🌧',
    '386': '朗', #⛈',
    '389': '朗', #🌩',
    '392': '朗', #⛈',
    '395': ''  #❄️'
}

if is_night:
    WEATHER_CODES['113'] = ''
    WEATHER_CODES['116'] = ''
    WEATHER_CODES['122'] = ''
    WEATHER_CODES['143'] = ''
    WEATHER_CODES['176'] = ''
    WEATHER_CODES['263'] = ''
    WEATHER_CODES['266'] = ''
    WEATHER_CODES['293'] = ''
    WEATHER_CODES['353'] = ''
    WEATHER_CODES['356'] = ''

data = {}


weather = requests.get("https://wttr.in/?format=j1").json()


def format_time(time):
    return time.replace("00", "").zfill(2)


def format_temp(temp):
    return (hour['FeelsLikeC']+"°").ljust(3)


def format_chances(hour):
    chances = {
        "chanceoffog": "Fog",
        "chanceoffrost": "Frost",
        "chanceofovercast": "Overcast",
        "chanceofrain": "Rain",
        "chanceofsnow": "Snow",
        "chanceofsunshine": "Sunshine",
        "chanceofthunder": "Thunder",
        "chanceofwindy": "Wind"
    }

    conditions = []
    for event in chances.keys():
        if int(hour[event]) > 0:
            conditions.append(chances[event]+" "+hour[event]+"%")
    return ", ".join(conditions)


if len(sys.argv) > 1:
    data["text"]  = weather['current_condition'][0]['FeelsLikeC'] + "°"
    data["class"] = "Temp"
else:
    data['text']  = WEATHER_CODES[weather['current_condition'][0]['weatherCode']]
    data["class"] = "t" + str(math.floor(max(int(weather['current_condition'][0]['FeelsLikeC'])+15,0)/5))

data['tooltip'] = f"<b>{weather['current_condition'][0]['weatherDesc'][0]['value']} {weather['current_condition'][0]['temp_C']}°</b>\n"
data['tooltip'] += f"Feels like: {weather['current_condition'][0]['FeelsLikeC']}°\n"
data['tooltip'] += f"Wind: {weather['current_condition'][0]['windspeedKmph']}Km/h\n"
data['tooltip'] += f"Humidity: {weather['current_condition'][0]['humidity']}%\n"

# for i, day in enumerate(weather['weather']):
day = weather['weather'][0]
data['tooltip'] += f"\n<b>"
    # if i == 0:
data['tooltip'] += "Today, "
    # if i == 1:
        # break
        # data['tooltip'] += "Tomorrow, "
data['tooltip'] += f"{day['date']}</b>\n"
data['tooltip'] += f"⬆️ {day['maxtempC']}° ⬇️ {day['mintempC']}° "
data['tooltip'] += f"🌅 {day['astronomy'][0]['sunrise']} 🌇 {day['astronomy'][0]['sunset']}\n"
for hour in day['hourly']:
    # if i == 0:
    if int(format_time(hour['time'])) < datetime.now().hour-2:
        continue
    data['tooltip'] += f"{format_time(hour['time'])} {WEATHER_CODES[hour['weatherCode']]} {format_temp(hour['FeelsLikeC'])} {hour['weatherDesc'][0]['value']}, {format_chances(hour)}\n"

print(json.dumps(data))
