from __future__ import annotations

from typing import TYPE_CHECKING

from apollo.conf import SENSORS

if TYPE_CHECKING:
    from decimal import Decimal
    from psycopg2.extensions import connection as Connection


def get_sensors_data(connection: Connection, limit: int = 500, offset: int = 0) -> list[dict]:
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM data ORDER BY created_at DESC LIMIT %s OFFSET %s", (limit, offset))
        return [{**item} for item in cursor.fetchall()]


def get_latest_sensors_data(connection: Connection) -> list[dict]:
    with connection.cursor() as cursor:
        result = []
        for sensor in SENSORS:
            cursor.execute("SELECT * FROM data WHERE sensor_id = %s ORDER BY created_at DESC", (sensor,))
            if item := cursor.fetchone():
                result.append({**item})
        return result


def save_sensors_data(connection: Connection, sensor_id: str, temp: Decimal, humidity: Decimal):
    with connection.cursor() as cursor:
        cursor.execute("INSERT INTO data (sensor_id, temp, humidity) VALUES (%s, %s, %s)", (sensor_id, temp, humidity))
        connection.commit()
