from decimal import Decimal

from fastapi import FastAPI
from pydantic import BaseModel

from apollo.database import get_sensors_data, save_sensors_data

app = FastAPI()


class Sensor(BaseModel):
    name: str
    temp: int
    humidity: Decimal


@app.get("/")
async def get():
    return get_sensors_data()


@app.post("/")
async def post(sensor: Sensor):
    save_sensors_data(sensor.name, sensor.temp, sensor.humidity)
