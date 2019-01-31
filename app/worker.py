import os
import sqlite3

import Adafruit_DHT
import Adafruit_MCP3008
import Adafruit_GPIO.SPI as SPI

SPI_PORT = 0
SPI_DEVICE = 0
DHT22_PIN = 4

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'db.sqlite')


def get_moisture_level()->int:
    mcp = Adafruit_MCP3008.MCP3008(
        spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE)
    )
    adc = mcp.read_adc(0)
    return 100 - adc / 10.24


def get_temp_humidity()->tuple:
    return Adafruit_DHT.read_retry(
        Adafruit_DHT.DHT22, DHT22_PIN
    )


def save_data(t: float, h: int, m: int):
    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO data (temp, humidity, moisture) VALUES (?, ?, ?)",
            (t, h, m)
        )
        connection.commit()


if __name__ == '__main__':
    moisture = get_moisture_level()
    humidity, temp = get_temp_humidity()
    save_data(temp, humidity, moisture)

    print('Temp: {:0.2f} *C, humidity: {:d}%, moisture: {:d}%'.format(
        temp, int(humidity), int(moisture)
    ))
