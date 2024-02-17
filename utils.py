import requests
from flask import session

from app import Weather, db
from app import app
import datetime

# ключ для верификации при запросе
my_key = 'e2b0ae915b3b416696f101323241702'


def request_temperature(city: str) -> float:
    request = requests.get(url=f'http://api.weatherapi.com/v1/current.json?key={my_key}&q={city}')
    temperature = request.json().get('current').get('temp_c')
    return float(temperature)

def fetch_weather(city: str) -> float:
    # weather = session.query(Weather).filter(Weather.city == city).first()
    # weather = Weather.query.filter(city == city)
    weather = Weather.get_weather(city)
    return weather
    # print(weather)
    # weather = None
    # if weather is None:
    #     temperature = request_temperature(city)
    #     weather = Weather(city, temperature, datetime.datetime.now())
    #     db.session.add(weather)
    #     db.session.commit()
    # else:
    #     print('from db', weather)
    #     print(weather.temperature, weather.datetime)
    # # print(temperature)


with app.app_context():
    fetch_weather('Minsk')




