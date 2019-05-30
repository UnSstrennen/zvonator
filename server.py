from flask import Flask, render_template, request, redirect
from main import ring


app = Flask(__name__)
app.config['SECRET_KEY'] = 'camel-kalmik228'


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html', ring_state=int(ring.state))


@app.route('/switch_ring', methods=['GET', 'POST'])
def switch_ring():
    global ring
    ring.switch()
    return redirect('/')


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
