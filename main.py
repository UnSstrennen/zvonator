from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from configparser import ConfigParser
from crontab import CronTab


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'camel-kalmik228'
db = SQLAlchemy(app)

config = ConfigParser()
config.read('config.ini')

cron = CronTab(user=config['linux_user']['username'])


class RingModel(db.Model):
    """ DB model of single ring """
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.Text(8), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    dow = db.Column(db.Text(27), nullable=False)
    comment = db.Column(db.Text(50), nullable=False)
    files_paths = db.Column(db.Text(1000), nullable=False)


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
        rings_to_set = RingModel.query.all()
        for ring_to_add in rings_to_set:
            start_time = ring_to_add.time.split(':')  # as list of hours, minutes and seconds
            hour, minute, second = start_time
            files_paths = ring_to_add.files_paths
            dow = ring_to_add.dow.split()
            command = 'sleep({}); python run.py {}'.format(int(second), ' '.join(files_paths))
            comment = config['cron']['comment_start'] + ' ' + ring_to_add.comment
            job = cron.new(command=command, comment=comment)  # TODO: check the command
            job.hour.on(hour)
            job.minute.on(minute)
            if dow != ['*']:
                job.dow.on(*dow)
        cron.write()

    def off(self):
        """ remove zvonator jobs from crontab """
        print('off')
        comment_start = config['cron']['comment_start']
        for job in cron:
            if job.comment.startswith(comment_start):
                cron.remove(job)
        cron.write()


db.create_all()
ring = Ring()
