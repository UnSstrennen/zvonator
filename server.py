from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename
from main import ring, db, config
import os
from string import punctuation


UPLOAD_DIR = config['play_settings']['sound_directory']
SUPPORTED_FORMATS = config['play_settings']['supported_formats'].split()


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


def valid_filename(filename):
    """ returns OK as string if filename is valid, else it returns error description as string """
    if len(filename) == 0:
        return 'Пустое имя файла!'
    if filename[0] in punctuation:
        return 'Имя файла не должно начинаться со знаков препинания!'
    format = filename.split('.')
    if format not in SUPPORTED_FORMATS:
        return 'Формат файла не поддерживается.'
    return 'OK'


@app.route('/upload', methods=['GET', 'POST', 'DELETE'])
def upload():
    if request.method == 'GET':
        return render_template('upload.html')
    elif request.method == 'POST':
        file = request.files['file']
        print(request.form.get('hours'))
        if file:
            filename = secure_filename(file.filename)
            valid = valid_filename(filename)
            file.save(os.path.join(UPLOAD_DIR, filename))
        return 'OK'
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


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
