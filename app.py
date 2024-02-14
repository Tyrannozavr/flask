from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'


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

  def __repr__(self):
        return f'<User {self.username}>'

with app.app_context():
    db.create_all()
    user = User('John', 2000)
    db.session.add(user)
    db.session.commit()

