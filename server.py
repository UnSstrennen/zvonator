from flask import Flask, render_template, request, redirect
from main import ring, db


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
    return render_template('upload.html')


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
