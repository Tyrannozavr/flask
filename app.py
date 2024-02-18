import asyncio
import datetime

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.future import engine
from sqlalchemy.util.preloaded import orm
from flask import request
from sqlalchemy import select

app = Flask(__name__)

if __name__ == 'main':
    app.run(debug=True)

# подключение базы данных
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

# an Engine, which the Session will use for connection
# resources
engine = create_engine("sqlite:///users.db")

# create session and add objects

class Weather(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(100))
    temperature = db.Column(db.Integer, unique=False, nullable=False)
    datetime = db.Column(db.DateTime, unique=False, nullable=False)

    def __init__(self, city, temperature, datetime):
        self.city = str(city)
        self.temperature = temperature
        self.datetime = datetime
        super().__init__()

    @classmethod
    def get_weather(cls, city):
        with Session(engine) as session:
            weather = Weather.query.filter_by(city=city).first()
        return weather


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    balance = db.Column(db.Integer, unique=False, nullable=False)

    def __init__(self, username, balance):
        self.username = username
        self.balance = balance
        super().__init__()

    @classmethod
    def add_user(cls, username, balance=None):
        if balance is None:
            balance = 6000
        balance = int(balance)
        user = cls(username, balance)
        db.session.add(user)
        db.session.commit()
        return user

    def update_user(self, username: str = None, balance: int = None):
        if username:
            self.username = username
        if balance:
            self.balance = int(balance)
        db.session.commit()
        return self

    @classmethod
    def delete_user(cls, user_id: int):
        user = cls.query.get(int(user_id))
        if user:
            db.session.delete(user)
            db.session.commit()
        else:
            raise 'User not found'

    @orm.validates('balance')
    def validate_balance(self, key, value):
        if value < 0:
            raise ValueError('balance cannot be negative')
        return value

    def __repr__(self):
        return f'<User {self.username}>'


# добавления, обновления и удаления пользователей и обновления их балансов

from utils import fetch_weather
@app.route('/update')
def update():
    # weather = Weather.get_weather('Minsk')
    coroutine = fetch_weather('Minsk')
    weather = asyncio.run(coroutine)
    date = weather.datetime
    different = datetime.datetime.now() - date
    # if different.total_seconds() > 300:
    #     print('old data')
        # new_weather =
    # print(different > datetime.time(minute=5))

    return jsonify(a='aaa')


with app.app_context():
    db.create_all()
    names = ['John', 'Smith', 'Mike', 'David', 'Jack']
    balances = [5000, 6000, 7000, 8000, 10000]
    query = User.query.all()
    if len(query) == 0:
        for name, balance in zip(names, balances):
            user = User(name, balance)
            db.session.add(user)
        db.session.commit()
