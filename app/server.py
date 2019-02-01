import json

from flask import (
    Flask,
    jsonify,
    render_template
)
from app.db import get_data

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html',
                           data=json.dumps(get_data()[0]),
                           options=get_data()[1])


@app.route('/api')
def api():
    return jsonify(get_data()[0])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
