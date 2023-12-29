import Adafruit_DHT
import logging.config
import psycopg2

from psycopg2.extras import DictCursor

from apollo.conf import DHT22_CHANNEL, LOGGING, DATABASE_URL
from apollo.database import save_sensors_data

logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)


if __name__ == "__main__":
    connection = psycopg2.connect(DATABASE_URL, cursor_factory=DictCursor)
    humidity, temp = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, DHT22_CHANNEL)
    save_sensors_data(connection=connection, sensor_id="CORUSCANT", temp=temp, humidity=humidity)
    logger.info(f"Temp: {temp} *C, humidity: {humidity}")
