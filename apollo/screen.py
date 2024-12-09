import logging.config

import psycopg2
from psycopg2.extras import DictCursor
from RPLCD.i2c import CharLCD

from apollo.conf import DATABASE_URL, LOGGING, MODE, ONE_WIRE_SENSORS, SATELLITES
from apollo.database import get_latest_sensors_data
from apollo.services import print_sensors_data


logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)


if __name__ == "__main__":
    connection = psycopg2.connect(DATABASE_URL, cursor_factory=DictCursor)
    sensors = SATELLITES.keys() if MODE == "network" else ONE_WIRE_SENSORS.keys()
    data = get_latest_sensors_data(connection=connection, sensors=sensors)
    result = print_sensors_data(data)

    lcd = CharLCD("PCF8574", 0x27)
    lcd.clear()
    lcd.write_string(result)
    logger.info(result)
