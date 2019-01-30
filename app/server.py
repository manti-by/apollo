import sqlite3

from flask import Flask, render_template

app = Flask(__name__)


def get_data()->list:
    with sqlite3.connect('data.db') as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM data LIMIT 10 ORDER BY datetime DESC")
        result = cursor.fetchall()
        connection.close()
        return result


@app.route('/')
def index():
    data = get_data()
    return render_template('index.html', data=data)


if __name__ == '__main__':
    app.run()
