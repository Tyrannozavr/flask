import asyncio
import datetime
import json
import threading


from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.future import engine
from sqlalchemy.util.preloaded import orm
from flask import request
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

app = Flask(__name__)

if __name__ == 'main':
    app.run(debug=True)

# подключение базы данных
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)




engine = create_engine("sqlite:///users.db")


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



# определение моделей
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

users = {}

# путь для запроса, принимает userId и city в качестве параметров
@app.route('/update')
def update_user_balance():
    userId = request.args.get('userId')
    city = request.args.get('city')
    try:
        coroutine = fetch_weather(city)
        temperature = asyncio.run(coroutine)
    except Exception as e:
        return json.dumps({'error': str(e)})
    user = User.query.get(int(userId))
    if user is None:
        return jsonify({'error': 'User not found'})
    local_user = users.get(userId)
    if local_user:
        users[userId]['balance'] += temperature
        users[userId]['count'] += 1
    else:
        users[userId] = {'balance': user.balance, 'time': datetime.datetime.now(), 'count': 1}
    asyncio.run(commit(userId))
    return jsonify(status=200)


# следующие две функции нужны для того, чтобы коммит применялся через секунду и применил данные при 1000 запросов в секунду
# без ошибок
def update_user(userId):
    with app.app_context():
        user = User.query.get(int(userId))
        balance = users[userId]['balance']
        if balance >= 0:
            user.balance = balance
        else:
            users[userId]['balance'] = 0
            user.balance = 0
        db.session.commit()


async def commit(userId):
    t = threading.Timer(1, update_user, args=(userId))
    t.start()


#Здесь создаем базу и наполняем
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
