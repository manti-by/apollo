import logging.config
import psycopg2

from RPLCD.i2c import CharLCD
from psycopg2.extras import DictCursor

from apollo.conf import LOGGING, DATABASE_URL, ONE_WIRE_SENSORS
from apollo.database import get_latest_sensors_data
from apollo.services import print_sensors_data

logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)


if __name__ == "__main__":
    connection = psycopg2.connect(DATABASE_URL, cursor_factory=DictCursor)
    sensors = ONE_WIRE_SENSORS.keys() + ["AIR"]
    data = get_latest_sensors_data(connection=connection, sensors=sensors)
    result = print_sensors_data(data)

    lcd = CharLCD("PCF8574", 0x27)
    lcd.clear()
    lcd.write_string(result)
    logger.info(result)
