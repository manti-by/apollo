import os
import sqlite3

from flask import request

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'db.sqlite')

PERIODS = {
    'live': 1,
    'hourly': 12,
    'daily': 12 * 24,
    'weekly': 12 * 24 * 7,
}


def get_line_chart_data()->tuple:
    _type = request.args.get('type', 'absolute')
    limit = request.args.get('limit', 10)
    group = request.args.get('group', 'hourly')

    with sqlite3.connect(DB_PATH) as session:
        cursor = session.cursor()
        query_limit = PERIODS.get(group, 1) * int(limit)
        cursor.execute(
            "SELECT * FROM data ORDER BY datetime DESC LIMIT ?", (query_limit, )
        )
        session.commit()
        data = cursor.fetchall()[::-1]

        result = {
            'temp': [],
            'humidity': [],
            'moisture': [],
            'label': [],
        }

        sum_temp = 0
        sum_humidity = 0
        sum_moisture = 0
        counter = 0

        period = PERIODS.get(group)
        for item in data:
            counter += 1
            sum_temp += item[1] or 0
            sum_humidity += item[2] or 0
            sum_moisture += item[3] or 0

            if group in ('live', 'hourly'):
                label = item[4][11:16]
            else:
                label = item[4][:10]

            if counter % period == 0:
                result['temp'].append(round(sum_temp / period, 1))
                result['humidity'].append(round(sum_humidity / period, 1))
                result['moisture'].append(round(sum_moisture / period, 1))
                result['label'].append(label)

                sum_temp = 0
                sum_humidity = 0
                sum_moisture = 0

        return result, {
            'type': _type,
            'limit': limit,
            'group': group
        }


def get_bar_chart_data():
    with sqlite3.connect(DB_PATH) as session:
        cursor = session.cursor()
        cursor.execute(
            "SELECT * FROM data ORDER BY datetime DESC LIMIT 1"
        )
        session.commit()
        return cursor.fetchone()
