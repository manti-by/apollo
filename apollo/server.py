from datetime import datetime
from decimal import Decimal
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel, Field

from apollo.conf import SENSORS
from apollo.database import get_latest_sensors_data, save_sensors_data, get_sensors_data

app = FastAPI()


class Sensor(BaseModel):
    sensor_id: str
    temp: Decimal
    humidity: Decimal
    created_at: Optional[datetime] = Field(None)


def filter_results(data):
    for item in data:
        item["temp"] = round(Decimal(item["temp"]) + SENSORS[item["sensor_id"]]["temp_offset"], ndigits=2)
        item["humidity"] = round(Decimal(item["humidity"]) + SENSORS[item["sensor_id"]]["humidity_offset"], ndigits=2)
    return data


@app.get("/")
async def get() -> list[Sensor]:
    original_data = get_latest_sensors_data()
    return filter_results(original_data)


@app.get("/batch/")
async def batch(limit: int = 500) -> list[Sensor]:
    original_data = get_sensors_data(limit=limit)
    return filter_results(original_data)


@app.post("/")
async def post(sensor: Sensor):
    save_sensors_data(sensor.sensor_id, sensor.temp, sensor.humidity)
