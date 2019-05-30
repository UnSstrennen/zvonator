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
        """ switch ring operating state to opposite mode"""
        self.state = not self.state
        self.on() if self.state else self.off()

    def on(self):
        """ create timemable for crontab and update it """
        print('on')
        pass

    def off(self):
        """ do crontab -r for stop operating """
        print('off')
        pass


ring = Ring()