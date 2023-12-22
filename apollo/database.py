from __future__ import annotations

import sqlite3
from decimal import Decimal
from sqlite3 import Cursor

from apollo.conf import DB_PATH, SENSORS

sqlite3.register_adapter(Decimal, lambda d: str(d))
sqlite3.register_converter("DECTEXT", lambda d: Decimal(d.decode("ascii")))


def dict_factory(cursor: Cursor, row: dict):
    result = {}
    for idx, col in enumerate(cursor.description):
        result[col[0]] = row[idx]
    return result


def get_sensors_data(limit: int = 500) -> list[dict]:
    with sqlite3.connect(DB_PATH, detect_types=sqlite3.PARSE_DECLTYPES) as session:
        session.row_factory = dict_factory
        cursor = session.cursor()
        cursor.execute("SELECT * FROM data ORDER BY created_at DESC LIMIT ?", (limit,))
        session.commit()
        return cursor.fetchall()


def get_latest_sensors_data() -> list[dict]:
    with sqlite3.connect(DB_PATH, detect_types=sqlite3.PARSE_DECLTYPES) as session:
        session.row_factory = dict_factory
        cursor = session.cursor()
        result = []
        for sensor in SENSORS:
            cursor.execute("SELECT * FROM data WHERE sensor_id = ? ORDER BY created_at DESC", (sensor,))
            session.commit()
            result.append(cursor.fetchone())
        return result


def save_sensors_data(sensor_id: str, temp: Decimal, humidity: Decimal):
    with sqlite3.connect(DB_PATH, detect_types=sqlite3.PARSE_DECLTYPES) as connection:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO data (sensor_id, temp, humidity) VALUES (?, ?, ?)", (sensor_id, temp, humidity))
        connection.commit()
