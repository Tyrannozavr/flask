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
async def task_coroutine():
    # вывод сообщения
    print('executing the task')
    # блокировка на некоторое время
    await asyncio.sleep(1)
async def refresh_data(city: str):
    temperature = request_temperature(city)
    weather = Weather.get_weather(city)
    weather.temperature = temperature
    weather.datetime = datetime.datetime.now()
    # db.session.add()
    db.session.commit()

async def fetch_weather(city: str) -> float:
    weather = Weather.get_weather(city)
    weather_datetime = weather.datetime
    different = datetime.datetime.now() - weather_datetime
    # if different.total_seconds() > 300:
    if True:
        print('run')
        asyncio.create_task(refresh_data(city))
        # task = asyncio.create_task(task_coroutine())
        print('end')
    return weather


with app.app_context():
    fetch_weather('Minsk')




