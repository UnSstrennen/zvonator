from flask_sqlalchemy import SQLAlchemy
from flask import Flask


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'camel-kalmik228'
db = SQLAlchemy(app)


class RingModel(db.Model):
    """ Описание единовременного звонка как сущности """
    id = db.Column(db.Integer, primary_key=True)
    # time = db.Column(db.)


class Ring:
    def __init__(self):
        self.state = False

    def switch(self):
        self.state = not self.state


ring = Ring()