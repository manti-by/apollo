from __future__ import annotations

import sqlite3
from decimal import Decimal
from sqlite3 import Cursor

from apollo.conf import DB_PATH


def dict_factory(cursor: Cursor, row: dict):
    result = {}
    for idx, col in enumerate(cursor.description):
        result[col[0]] = row[idx]
    return result


def get_sensors_data() -> dict:
    with sqlite3.connect(DB_PATH) as session:
        session.row_factory = dict_factory
        cursor = session.cursor()
        cursor.execute("SELECT name, temp, humidity FROM data ORDER BY datetime DESC")
        session.commit()
        return cursor.fetchone()


def save_sensors_data(name: str, temp: int, humidity: Decimal):
    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO data (name, temp, humidity) VALUES (?, ?, ?)", (name, temp, humidity))
        connection.commit()
