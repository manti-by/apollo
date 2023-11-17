from decimal import Decimal

from fastapi import FastAPI
from pydantic import BaseModel

from apollo.database import get_sensors_data, save_sensors_data

app = FastAPI()


class Sensor(BaseModel):
    sensor_id: str
    temp: Decimal
    humidity: Decimal


@app.get("/")
async def get():
    return get_sensors_data()


@app.post("/")
async def post(sensor: Sensor):
    save_sensors_data(sensor.sensor_id, sensor.temp, sensor.humidity)
