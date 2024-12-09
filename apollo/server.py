import logging.config
from datetime import datetime
from decimal import Decimal

import psycopg2
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from psycopg2.extras import DictCursor
from pydantic import BaseModel, Field

from apollo.conf import DATABASE_URL, LOGGING, ONE_WIRE_SENSORS, SATELLITES
from apollo.database import get_latest_sensors_data, get_sensors_data, save_sensors_data
from apollo.services import print_sensors_data


logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)

connection = psycopg2.connect(DATABASE_URL, cursor_factory=DictCursor)
app = FastAPI()


class Sensor(BaseModel):
    id: int | None = Field(None)
    created_at: datetime | None = Field(None)

    sensor_id: str
    temp: Decimal
    humidity: Decimal | None = None


def adjust_values(items: list) -> list[Sensor]:
    result = []
    sensors = {**SATELLITES, **ONE_WIRE_SENSORS}
    for item in items:
        sensor = sensors.get([item["sensor_id"]])
        if sensor is None:
            logger.warning(f"Sensor {item['sensor_id']} not found")
            continue

        if sensor.get("temp_offset"):
            item["temp"] = round(Decimal(item["temp"]) + sensor.get("temp_offset"), ndigits=1)
        if item.get("humidity") and sensor.get("humidity_offset"):
            item["humidity"] = round(Decimal(item["humidity"]) + sensor.get("temp_offset"), ndigits=1)

        result.append(Sensor(**item))
    return result


@app.get("/")
async def get(mode: str | None = "local") -> list[Sensor]:
    sensors = SATELLITES.keys() if mode == "network" else ONE_WIRE_SENSORS.keys()
    original_data = get_latest_sensors_data(connection=connection, sensors=sensors)
    return adjust_values(original_data)


@app.get("/print/", response_class=PlainTextResponse)
async def echo(mode: str | None = "local") -> str:
    sensors = SATELLITES.keys() if mode == "network" else ONE_WIRE_SENSORS.keys()
    original_data = get_latest_sensors_data(connection=connection, sensors=sensors)
    return print_sensors_data(adjust_values(original_data))


@app.get("/batch/")
async def batch(limit: int = 500, offset: int = 0) -> list[Sensor]:
    original_data = get_sensors_data(connection=connection, limit=limit, offset=offset)
    return adjust_values(original_data)


@app.post("/")
async def post(sensor: Sensor):
    save_sensors_data(connection=connection, sensor_id=sensor.sensor_id, temp=sensor.temp, humidity=sensor.humidity)
    return "Created"
