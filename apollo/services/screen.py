import logging.config

import psycopg2
from apollo.services import print_sensors_data
from apollo.services.database import get_latest_sensors_data
from apollo.services.models import Sensor
from apollo.settings import DATABASE_URL, LOGGING, SENSORS
from psycopg2.extras import DictCursor
from RPLCD.i2c import CharLCD


logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)


if __name__ == "__main__":
    connection = psycopg2.connect(DATABASE_URL, cursor_factory=DictCursor)
    sensor_ids = [x.sensor_id for x in SENSORS.values()]
    data = get_latest_sensors_data(connection=connection, sensor_ids=sensor_ids)
    result = print_sensors_data([Sensor(**x) for x in data])

    lcd = CharLCD("PCF8574", 0x27)
    lcd.clear()
    lcd.write_string(result)
    logger.info(result)
