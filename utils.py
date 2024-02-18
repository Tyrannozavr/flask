from app import Weather, db
import datetime
import asyncio

# ключ для верификации при запросе
my_key = 'e2b0ae915b3b416696f101323241702'


def request_temperature(city: str) -> float:
    request = requests.get(url=f'http://api.weatherapi.com/v1/current.json?key={my_key}&q={city}')
    temperature = request.json().get('current').get('temp_c')
    return float(temperature)

# обновляет данные в бд по температуре в городе, по задумке без задержки запроса
async def refresh_data(city: str):
    temperature = request_temperature(city)
    weather = Weather.get_weather(city)
    if weather is None:
        weather = Weather(city, temperature, datetime.datetime.now())
        db.session.add(weather)
    else:
        weather.temperature = temperature
        weather.datetime = datetime.datetime.now()
    db.session.commit()


async def fetch_weather(city: str) -> float:
    weather = Weather.get_weather(city)
    if weather is None:  # если данных в кэше нет - записываем и после возвращаем
        await asyncio.create_task(refresh_data(city))
        weather = Weather.get_weather(city)
    else:
        weather_datetime = weather.datetime
        different = datetime.datetime.now() - weather_datetime
        if different.total_seconds() > 540:  # если прошло более 9 минут ждем обновления данных и после этого возвращаем
            await refresh_data(city)
            weather = Weather.get_weather(city)
        elif different.total_seconds() > 300:  # при регулярных запросах раз в 5 минут обновляются данные
            asyncio.create_task(refresh_data(city))
    return weather.temperature
