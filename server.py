from flask import Flask, render_template, request
from main import Ring
# from forms


app = Flask(__name__)

ring = Ring()


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    global ring
    if request.method == 'POST':
        print(request.method)
        ring.switch()
    return render_template('index.html', ring_state=ring.state)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
