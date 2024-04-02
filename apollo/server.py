import psycopg2

from datetime import datetime
from decimal import Decimal
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel, Field
from psycopg2.extras import DictCursor

from apollo.conf import SENSORS, DATABASE_URL
from apollo.database import get_latest_sensors_data, save_sensors_data, get_sensors_data

connection = psycopg2.connect(DATABASE_URL, cursor_factory=DictCursor)
app = FastAPI()


class Sensor(BaseModel):
    id: Optional[int] = Field(None)
    created_at: Optional[datetime] = Field(None)

    sensor_id: str
    temp: Decimal


def filter_results(data):
    for item in data:
        item["temp"] = round(Decimal(item["temp"]) + SENSORS[item["sensor_id"]]["offset"], ndigits=2)
    return data


@app.get("/")
async def get() -> list[Sensor]:
    original_data = get_latest_sensors_data(connection=connection)
    return filter_results(original_data)


@app.get("/batch/")
async def batch(limit: int = 500, offset: int = 0) -> list[Sensor]:
    original_data = get_sensors_data(connection=connection, limit=limit, offset=offset)
    return filter_results(original_data)


@app.post("/")
async def post(sensor: Sensor):
    save_sensors_data(connection=connection, sensor_id=sensor.sensor_id, temp=sensor.temp)
    return "Created"
