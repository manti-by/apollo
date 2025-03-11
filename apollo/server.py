import logging.config

import psycopg2
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from psycopg2.extras import DictCursor

from apollo.conf import DATABASE_URL, LOGGING, MODE, SENSORS
from apollo.database import get_latest_sensors_data, get_sensors_data, save_sensors_data
from apollo.models import Sensor
from apollo.services import print_sensors_data


logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)

connection = psycopg2.connect(DATABASE_URL, cursor_factory=DictCursor)
app = FastAPI()


@app.get("/")
async def get() -> list[Sensor]:
    sensor_ids = [x.sensor_id for x in SENSORS.values()]
    return [Sensor(**x) for x in get_latest_sensors_data(connection=connection, sensor_ids=sensor_ids)]


@app.get("/print/", response_class=PlainTextResponse)
async def echo() -> str:
    sensor_ids = [x.sensor_id for x in SENSORS.values()]
    original_data = [Sensor(**x) for x in get_latest_sensors_data(connection=connection, sensor_ids=sensor_ids)]
    return print_sensors_data(original_data)


@app.get("/batch/")
async def batch(limit: int = 500, offset: int = 0) -> list[Sensor]:
    return [Sensor(**x) for x in get_sensors_data(connection=connection, limit=limit, offset=offset)]


@app.post("/")
async def post(sensor: Sensor):
    save_sensors_data(connection=connection, sensor_id=sensor.sensor_id, temp=sensor.temp, context={"mode": MODE})
    return "Created"
