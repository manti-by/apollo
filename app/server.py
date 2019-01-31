import os
import json
import sqlite3

from flask import (
    Flask,
    jsonify,
    render_template
)

app = Flask(__name__)

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'db.sqlite')


def get_data()->dict:
    with sqlite3.connect(DB_PATH) as session:
        cursor = session.cursor()
        cursor.execute("SELECT * FROM data ORDER BY datetime DESC LIMIT 10")
        session.commit()
        data = cursor.fetchall()[::-1]
        return {
            'temp': [x[1] for x in data],
            'humidity': [x[2] for x in data],
            'moisture': [x[3] for x in data],
            'label': [x[4][11:16] for x in data],
        }


@app.route('/')
def index():
    return render_template('index.html',
                           data=json.dumps(get_data()))


@app.route('/api')
def api():
    return jsonify(get_data())


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
