import Adafruit_DHT
import logging.config
from decimal import Decimal

import psycopg2

from pi1wire import Pi1Wire, Resolution
from psycopg2.extras import DictCursor

from apollo.conf import DHT22_CHANNEL, LOGGING, DATABASE_URL, ONE_WIRE_SENSORS
from apollo.database import save_sensors_data

logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)


if __name__ == "__main__":
    connection = psycopg2.connect(DATABASE_URL, cursor_factory=DictCursor)

    humidity, temp = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, DHT22_CHANNEL)
    save_sensors_data(connection=connection, sensor_id="CORUSCANT", temp=temp, humidity=humidity)
    logger.info(f"Temp for IAM: {temp} *C, humidity: {humidity}")

    wire = Pi1Wire()
    for sensor_id, data in ONE_WIRE_SENSORS.items():
        sensor = wire.find(data["address"])
        sensor.change_resolution(resolution=Resolution.X0_25)
        temp = round(Decimal(sensor.get_temperature()), 2)
        save_sensors_data(connection=connection, sensor_id=sensor_id, temp=temp)
        logger.info(f"Temp for {sensor_id}: {temp} *C")
