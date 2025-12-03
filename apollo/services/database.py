from __future__ import annotations

import json
from datetime import datetime
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from decimal import Decimal

    from psycopg2.extensions import connection as Connection  # noqa


def get_sensors_data(
    connection: Connection, limit: int = 500, offset: int = 0, sensor_id: str | None = None
) -> list[dict]:
    with connection.cursor() as cursor:
        params = (limit, offset)
        sql = "SELECT * FROM data ORDER BY created_at DESC LIMIT %s OFFSET %s"
        if sensor_id is not None:
            params = (sensor_id, limit, offset)
            sql = "SELECT * FROM data WHERE sensor_id = %s ORDER BY created_at DESC LIMIT %s OFFSET %s"
        cursor.execute(sql, params)
        return [{**item} for item in cursor.fetchall()]


def get_not_synced_sensors_data(connection: Connection, limit: int = 500, offset: int = 0) -> list[dict]:
    with connection.cursor() as cursor:
        params = (limit, offset)
        sql = "SELECT * FROM data WHERE synced_at IS NULL ORDER BY created_at DESC LIMIT %s OFFSET %s"
        cursor.execute(sql, params)
        return [{**item} for item in cursor.fetchall()]


def get_latest_sensors_data(connection: Connection, sensor_ids: list[str]) -> list[dict]:
    with connection.cursor() as cursor:
        result = []
        for sensor_id in sensor_ids:
            cursor.execute("SELECT * FROM data WHERE sensor_id = %s ORDER BY created_at DESC", (sensor_id,))
            if item := cursor.fetchone():
                result.append({**item})
        return result


def save_sensors_data(connection: Connection, sensor_id: str, temp: Decimal, context: dict | None = None):
    with connection.cursor() as cursor:
        cursor.execute(
            "INSERT INTO data (sensor_id, temp, context) VALUES (%s, %s, %s)",
            (sensor_id, temp, json.dumps(context) if context else "{}"),
        )
        connection.commit()


def update_sensor_data(
    connection: Connection,
    record_id: int,
    temp: Decimal,
    context: dict | None = None,
    synced_at: datetime | None = None,
):
    with connection.cursor() as cursor:
        cursor.execute(
            "UPDATE data SET temp = %s, context = %s, synced_at = %s WHERE id = %s",
            (temp, json.dumps(context) if context else "{}", synced_at, record_id),
        )
        connection.commit()
