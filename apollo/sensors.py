import logging.config
import Adafruit_DHT

from apollo.conf import DHT22_CHANNEL, LOGGING
from apollo.database import save_sensors_data

logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)


if __name__ == "__main__":
    humidity, temp = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, DHT22_CHANNEL)
    save_sensors_data("main", temp, humidity)
    logger.info(f"Temp: {temp} *C, humidity: {humidity}")
