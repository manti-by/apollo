import json
import sqlite3

from flask import Flask, render_template

app = Flask(__name__)


def get_data()->list:
    with sqlite3.connect('db.sqlite') as session:
        cursor = session.cursor()
        cursor.execute("SELECT * FROM data ORDER BY datetime DESC LIMIT 10")
        session.commit()
        return cursor.fetchall()


@app.route('/')
def index():
    data = get_data()[::-1]
    chart = json.dumps({
        'temp': [x[1] for x in data],
        'humidity': [x[2] for x in data],
        'moisture': [x[3] for x in data],
        'label': [x[4][11:16] for x in data],
    })
    return render_template('index.html', data=data, chart=chart)


if __name__ == '__main__':
    app.run()
