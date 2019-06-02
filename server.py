from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename
from main import ring, db, config
from os import path


UPLOAD_DIR = config['play_settings']['sound_directory']


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
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


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'GET':
        return render_template('upload.html')
    elif request.method == 'POST':
        file = request.files['file']
        print(request.form.get('hours'))
        return '11111'
        if file:
            filename = secure_filename(file.filename)
            file.save(path.join(UPLOAD_DIR, filename))
        return 'OK'


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
