import logging.config
from decimal import Decimal

import Adafruit_DHT
import psycopg2
from pi1wire import Pi1Wire, Resolution
from psycopg2.extras import DictCursor

from apollo.conf import DATABASE_URL, DHT22_CHANNEL, LOGGING, ONE_WIRE_SENSORS
from apollo.database import save_sensors_data


logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)


if __name__ == "__main__":
    connection = psycopg2.connect(DATABASE_URL, cursor_factory=DictCursor)

    humidity, temp = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, DHT22_CHANNEL)
    save_sensors_data(connection=connection, sensor_id="CORUSCANT", temp=temp, humidity=humidity)
    logger.info(f"Temp for IAM: {temp:2.1f} *C, humidity: {humidity:2.1f}%")

    wire = Pi1Wire()
    for sensor_id, data in ONE_WIRE_SENSORS.items():
        sensor = wire.find(data["address"])
        sensor.change_resolution(resolution=Resolution.X0_25)
        temp = round(Decimal(sensor.get_temperature()), 2) + data["temp_offset"]
        save_sensors_data(connection=connection, sensor_id=sensor_id, temp=temp)
        logger.info(f"Temp for {sensor_id}: {temp} *C")
