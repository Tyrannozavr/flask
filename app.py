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

    def add_user(self, username):
        pass

    def update_user(self, username=None, balance=None):
        if self.query.filter_by(username=username).first() and self.username != username:
            raise ValueError('username already taken')
        else:
            self.username = username
            self.balance = balance
            db.session.commit()
            return self

    @orm.validates('balance')
    def validate_age(self, key, value):
        if value < 0:
            raise ValueError('balance cannot be negative')
        return value

    def __repr__(self):
        return f'<User {self.username}>'


# добавления, обновления и удаления пользователей и обновления их балансов
from flask import request


@app.route('/update/<id>')
def update(id):
    user = User.query.get(id)
    username = request.args.get('username', user.username)
    balance = int(request.args.get('balance', user.balance))
    if user is None:
        return 'User not found'
    try:
        user = user.update_user(username, balance)
        return jsonify({'username': user.username, 'balance': user.balance})
    except ValueError as err:
        if err.args[0] == 'username already taken':
            return 'username already taken'
        elif err.args[0] == 'balance cannot be negative':
            return 'balance cannot be negative'


with app.app_context():
    db.create_all()
    names = ['John', 'Smith', 'Mike', 'David', 'Jack']
    balances = [5000, 6000, 7000, 8000, 10000]
    query = User.query.all()
    if len(query) == 0:
        for name, price in zip(names, balances):
            user = User(name, price)
            db.session.add(user)
        db.session.commit()
