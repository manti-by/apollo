import logging.config
from decimal import Decimal

import psycopg2
from apollo.services.database import save_sensors_data
from apollo.settings import DATABASE_URL, LOGGING, MODE, SENSORS
from pi1wire import NotFoundSensorException, Pi1Wire, Resolution
from psycopg2.extras import DictCursor


logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)


if __name__ == "__main__":
    wire = Pi1Wire()
    connection = psycopg2.connect(DATABASE_URL, cursor_factory=DictCursor)

    for sensor_id, sensor in SENSORS.items():
        try:
            wire_sensor = wire.find(sensor.sensor_id)
        except NotFoundSensorException:
            logger.info(f"{sensor_id} not found")
            continue

        wire_sensor.change_resolution(resolution=Resolution.X0_25)
        temp = round(Decimal(wire_sensor.get_temperature()), 2)

        save_sensors_data(connection=connection, sensor_id=sensor.sensor_id, temp=temp, context={"mode": MODE})
        logger.info(f"Temp for {sensor.label}: {temp} *C")
