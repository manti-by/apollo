import psycopg2

from datetime import datetime
from decimal import Decimal

from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel, Field
from psycopg2.extras import DictCursor

from apollo.conf import SATELLITES, DATABASE_URL, ONE_WIRE_SENSORS
from apollo.database import get_latest_sensors_data, save_sensors_data, get_sensors_data
from apollo.services import print_sensors_data

connection = psycopg2.connect(DATABASE_URL, cursor_factory=DictCursor)
app = FastAPI()


class Sensor(BaseModel):
    id: int | None = Field(None)
    created_at: datetime | None = Field(None)

    sensor_id: str
    temp: Decimal
    humidity: Decimal | None = None


def get_fixed_temp(item: dict) -> Decimal:
    return round(Decimal(item["temp"]) + SATELLITES[item["sensor_id"]]["offset"], ndigits=1)


@app.get("/")
async def get() -> dict[str, Sensor]:
    original_data = get_latest_sensors_data(connection=connection, sensors=SATELLITES.keys())
    for _, item in original_data.items():
        item["temp"] = get_fixed_temp(item)
    return original_data


@app.get("/print/", response_class=PlainTextResponse)
async def print() -> str:
    sensors = ONE_WIRE_SENSORS.keys() + ["AIR"]
    original_data = get_latest_sensors_data(connection=connection, sensors=sensors)
    for _, item in original_data.items():
        item["temp"] = get_fixed_temp(item)
    return print_sensors_data(original_data)


@app.get("/batch/")
async def batch(limit: int = 500, offset: int = 0) -> list[Sensor]:
    original_data = get_sensors_data(connection=connection, limit=limit, offset=offset)
    for item in original_data:
        item["temp"] = get_fixed_temp(item)
    return original_data


@app.post("/")
async def post(sensor: Sensor):
    save_sensors_data(connection=connection, sensor_id=sensor.sensor_id, temp=sensor.temp, humidity=sensor.humidity)
    return "Created"
