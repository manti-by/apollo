import logging.config
from datetime import datetime

import RPi.GPIO as GPIO
import psycopg2

from RPLCD.gpio import CharLCD
from psycopg2.extras import DictCursor

from apollo.conf import LOGGING, DATABASE_URL
from apollo.database import get_latest_sensors_data

logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)


if __name__ == "__main__":
    connection = psycopg2.connect(DATABASE_URL, cursor_factory=DictCursor)
    sensors = get_latest_sensors_data(connection=connection)

    result = datetime.now().strftime("%H:%M:%S %d-%m-%Y") + "\n"
    for sensor in get_latest_sensors_data(connection=connection):
        result += f"{sensor['sensor_id']}: {round(sensor['temp'], 2)} *C\n"
    logger.info(result)

    lcd = CharLCD(pin_rs=15, pin_rw=18, pin_e=16, pins_data=[21, 22, 23, 24], numbering_mode=GPIO.BOARD)
    lcd.clear()
    lcd.write_string(result)
