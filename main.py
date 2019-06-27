from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from configparser import ConfigParser
from crontab import CronTab


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'camel-kalmik228'
db = SQLAlchemy(app)
db.init_app(app)

config = ConfigParser()
config.read('config.ini')

# cron = CronTab(user=config['linux_user']['username'])


class Rings(db.Model):
    """ DB model of single ring """
    id = db.Column(db.Integer, primary_key=True)
    start_hour = db.Column(db.Integer, nullable=False)
    start_minute = db.Column(db.Integer, nullable=False)
    start_second = db.Column(db.Integer, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    dow = db.Column(db.Text(27), nullable=False)
    comment = db.Column(db.Text(50), nullable=False)
    files_paths = db.Column(db.Text(1000), nullable=False)


asdadqfwgfqgaw = Rings.query.all()


class Ring:
    def __init__(self):
        self.state = False

    def switch(self):
        """ switch ring operating state to opposite mode """
        self.state = not self.state
        self.on() if self.state else self.off()

    def on(self):
        """ create timemable for crontab and update it """
        print('on')
        amplifier_booting_duration = int(config['amplifier']['boot_duration'])
        rings_to_set = Rings.query.all()
        for ring_to_add in rings_to_set:
            hour, minute, second = ring_to_add.start_hour, ring_to_add.start_minute, ring_to_add.start_second
            files_paths = ring_to_add.files_paths.split(';')
            dow = ring_to_add.dow.split()
            hour, minute, second, need_to_shift_dow = self.sub_ring_time(
                hour, minute, second, amplifier_booting_duration)
            if need_to_shift_dow:
                self.shift_dow(dow)
            command = 'sleep({}); python run.py {};'.format(int(second), ' '.join(files_paths))
            comment = config['cron']['comment_start'] + ' ' + ring_to_add.comment
            continue
            job = cron.new(command=command, comment=comment)  # TODO: check the command
            job.hour.on(hour)
            job.minute.on(minute)
            if dow != ['*']:
                job.dow.on(*dow)
        return
        cron.write()

    def off(self):
        """ remove zvonator jobs from crontab """
        print('off')
        comment_start = config['cron']['comment_start']
        return
        for job in cron:
            if job.comment.startswith(comment_start):
                cron.remove(job)
        cron.write()

    def collide(self, start_hour_1, start_minute_1, start_second_1, duration_1,
                start_hour_2, start_minute_2, start_second_2, duration_2):
        start_time_1 = start_hour_1 * 3600 + start_minute_1 * 60 + start_second_1
        start_time_2 = start_hour_2 * 3600 + start_minute_2 * 60 + start_second_2
        end_time_1 = start_time_1 + duration_1
        end_time_2 = start_time_2 + duration_2
        if start_time_1 <= start_time_2 <= end_time_1 or start_time_1 <= end_time_2 <= end_time_1 or \
                start_time_2 <= start_time_1 <= end_time_2:
            return True
        return False

    def sub_ring_time(self, hour, minute, sec, sec_to_subtract):
        flag = False
        # make seconds as days
        time = hour * 3600 + minute * 60 + sec
        time -= sec_to_subtract
        if time < 0:
            time = 86400 - abs(time)
            flag = True
        # convert time in seconds to normal time
        hour = time // 3600
        time -= hour * 3600
        minute = time // 60
        time -= minute * 60
        sec = time
        return hour, minute, sec, flag

    def shift_dow(self, dow):
        weekdays = ['SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT']
        res = list()
        if dow == ['*']:
            return ['*']
        for weekday in dow:
            res.append(weekdays[weekdays.index(weekday) - 1])
        return res

    def set_from_form(self, form_data):
        """ gets form data as form_data argument and creates crontab event
        form_data keys manual:
        * repeat (required, any mode) - sets the repeating mode for rings.
            Also, using this data you can understand, what keys you can get then
        * date (only if repeat is set to 'no') - date DD-MM-YYYY
        * time (any mode) - time HH-MM-SS
        *comment (any mode) - comment as plain text in str format
        * month (one month in str format if repeat is set to 'every_year'
            or list of months if repeat is set to 'on_selected_days_of_months') - month
            in three-letters format (first 3 letters in the name of month in upper case
            for example, JAN means January)
        * day (one day in str format if repeat is set to 'every_year' or list of days
            if repeat is set to 'on_selected_days_of_months' or 'every_month') - day(s)
            of month in str format as numbers
        * dows (list of days of week if repeat is set to 'on_selected_dows') - day(s) of week
            if three-letters format (first 3 letters in the name of day of week in upper case
            for example, MON means Monday)
         """
        # TODO: fill a function. Raise an error if repeat data is null
        return


db.create_all()
ring = Ring()
