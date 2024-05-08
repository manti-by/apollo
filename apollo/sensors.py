import logging.config
from decimal import Decimal

import psycopg2

from pi1wire import Pi1Wire, Resolution
from psycopg2.extras import DictCursor

from apollo.conf import LOGGING, DATABASE_URL, SENSORS
from apollo.database import save_sensors_data

logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)


if __name__ == "__main__":
    connection = psycopg2.connect(DATABASE_URL, cursor_factory=DictCursor)
    wire = Pi1Wire()
    for sensor_id, data in SENSORS.items():
        sensor = wire.find(data["address"])
        sensor.change_resolution(resolution=Resolution.X0_25)
        temp = round(Decimal(sensor.get_temperature()), 2)
        save_sensors_data(connection=connection, sensor_id=sensor_id, temp=temp)
        logger.info(f"Temp for {sensor_id}: {temp} *C")
