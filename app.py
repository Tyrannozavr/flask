from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.util.preloaded import orm

app = Flask(__name__)

if __name__ == 'main':
    app.run(debug=True)

# подключение базы данных
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)


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


    def update_user(self, username=None, balance=None):
        if username and self.query.filter_by(username=username).first() and self.username != username:
            raise ValueError('username already taken')
        else:
            if username:
                self.username = username
            if balance:
                self.balance = int(balance)
            db.session.commit()
            return self

    @classmethod
    def delete_user(cls, user_id):
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
from flask import request


@app.route('/update')
def update():
    username = request.args.get('username')
    balance = request.args.get('balance')
    user = User.add_user(username, balance)
    return jsonify({'user': {'username': user.username, 'balance': user.balance}})

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
