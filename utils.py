import requests
from flask import session

from app import Weather, db
from app import app
import datetime
import asyncio

# ключ для верификации при запросе
my_key = 'e2b0ae915b3b416696f101323241702'


def request_temperature(city: str) -> float:
    request = requests.get(url=f'http://api.weatherapi.com/v1/current.json?key={my_key}&q={city}')
    temperature = request.json().get('current').get('temp_c')
    return float(temperature)


async def refresh_data(city: str):
    temperature = request_temperature(city)
    weather = Weather.get_weather(city)
    # print('weather in refresh is ', weather)
    if weather is None:
        weather = Weather(city, temperature, datetime.datetime.now())
        print(weather, 'now')
        db.session.add(weather)
    else:
        weather.temperature = temperature
        weather.datetime = datetime.datetime.now()
    db.session.commit()

async def fetch_weather(city: str) -> float:
    weather = Weather.get_weather(city)
    if weather is None:
        print('is none')
        await asyncio.create_task(refresh_data(city))
        print('await')
        weather = Weather.get_weather(city)
        print(weather)
    print('after if')
    weather_datetime = weather.datetime
    print('after weather datetime')
    different = datetime.datetime.now() - weather_datetime
    if different.total_seconds() > 6000:
        await refresh_data(city)
        weather = Weather.get_weather(city)
        print('fetch data')
    elif different.total_seconds() > 3000:
        asyncio.create_task(refresh_data(city))
        print('refresh data')
    print('end')
    return weather


with app.app_context():
    fetch_weather('Minsk')




