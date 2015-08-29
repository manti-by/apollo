import logging
import RPi.GPIO as GPIO
from flask import Flask, jsonify, request

from utils import get_onewire_value


app = Flask(__name__)
app.config.from_object('config')


@app.route("/")
def index():
    try:
        result = {
            'status'    : 200,
            'result'    : {
                'term_01' : get_onewire_value(app.config['TERM_01']),
                'term_02' : get_onewire_value(app.config['TERM_02'])
            }
        }
    except Exception as e:
        result = {
            'status'    : 500,
            'message'   : e.message
        }
    return jsonify(result)


@app.route('/shutdown', methods=['POST'])
def shutdown():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        return jsonify({
            'status'    : 500,
            'message'   : 'Not running with the Werkzeug Server'
        })

    func()
    return jsonify({
        'status'    : 200,
        'message'   : 'Server shutting down...'
    })


if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(app.config['TERM_INPUT'], GPIO.IN)
    app.run(host=app.config['HOST'], debug=app.config['DEBUG'])
