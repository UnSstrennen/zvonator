from flask import Flask, render_template, request, redirect, session
from werkzeug.utils import secure_filename
from main import ring, db, config, user
import os
from string import punctuation


UPLOAD_DIR = config['play_settings']['sound_directory']
SUPPORTED_FORMATS = config['play_settings']['supported_formats'].split()


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://{}:{}@{}/{}'.format(config['database']['username'], config['database']['password'], config['database']['ip'], config['database']['db_name'])
print(app.config['SQLALCHEMY_DATABASE_URI'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'camel-kalmik228'
db.init_app(app)


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html', ring_state=int(ring.state))


@app.route('/switch_ring', methods=['GET', 'POST'])
def switch_ring():
    ring.switch()
    return redirect('/')


@app.route('/upload', methods=['GET', 'POST', 'DELETE'])
def upload():
    if request.method == 'GET':
        supported_formats_str = ' '.join(SUPPORTED_FORMATS)
        return render_template('upload.html', SUPPORTED_FORMATS=supported_formats_str)
    elif request.method == 'POST':
        try:
            file = request.files['file']
        except KeyError:
            file = False
        if file:
            print("FILE!")
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_DIR, filename))
            return 'OK'
        else:
            ring.set_from_form(request.form)
            return '12345'
    elif request.method == 'DELETE':
        try:
            track_to_delete = request.json['name']
            path = UPLOAD_DIR + track_to_delete
            os.remove(path)
            return 'OK'
        except KeyError:
            return 'ERROR: Bad request'
        except FileNotFoundError:
            return 'ERROR: There is no file named {} on the server'.format(track_to_delete)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if not username or not password:
            return render_template('login.html', error=True)
        log = user.check_user(username, password)
        if not str(log).startswith('error'):
            # ok, log user in
            session['user_id'] = log  # id is storaged at the log if ok
            return redirect('/home')
        else:
            return render_template('login.html', error=True)
    if not session.get('user_id', False):
        # login is required
        return render_template('login.html', error=False)
    else:
        # login is not required, redirect to main page
        return redirect('/home')


@app.route('/home', methods=['GET', 'POST'])
def home():
    # if there is no user logged in
    if not session.get('user_id', False):
        return redirect('/login')
    return 'home there...'


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('user_id', None)
    return redirect('/')


@app.route('/register', methods=['GET', 'POST'])
def register():
    token = request.args.get('token')
    if token is None:
        return redirect('/home')


if __name__ == '__main__':
    app.run(port=5000, host='127.0.0.1')