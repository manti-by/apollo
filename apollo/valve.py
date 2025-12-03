import logging
import logging.config
import os
import time
from decimal import Decimal

import RPi.GPIO as GPIO
from apollo.settings import LOGGING
from pi1wire import NotFoundSensorException, Pi1Wire, Resolution


logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)

SENSOR_ID = os.getenv("VALVE_SENSOR_ID", "28000007173569")

RELAY_HEAT_PIN = 11
RELAY_COOL_PIN = 13

MODE_HEAT = "heat"
MODE_COOL = "cool"

TARGET_TEMP = Decimal("27.0")
HYSTERESIS = Decimal("1.0")
ACT_INTERVAL = Decimal("60.0")


def setup_gpio() -> None:
    GPIO.setmode(GPIO.BOARD)

    GPIO.setup(RELAY_HEAT_PIN, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(RELAY_COOL_PIN, GPIO.OUT, initial=GPIO.LOW)

    logger.info(f"GPIO initialised: HEAT={RELAY_HEAT_PIN}, COOL={RELAY_COOL_PIN} (BOARD numbering)")


def set_valve_mode(mode: str) -> None:
    if mode == MODE_HEAT:
        GPIO.output(RELAY_HEAT_PIN, GPIO.HIGH)
    else:
        GPIO.output(RELAY_COOL_PIN, GPIO.HIGH)

    logger.info(f"Setting valve mode set to {mode}")
    time.sleep(ACT_INTERVAL)
    logger.info(f"Successfully set valve mode to {mode}")

    GPIO.output(RELAY_HEAT_PIN, GPIO.LOW)
    GPIO.output(RELAY_COOL_PIN, GPIO.LOW)


def read_temperature() -> Decimal | None:
    try:
        wire = Pi1Wire()
        sensor = wire.find(SENSOR_ID)
    except NotFoundSensorException:
        logger.error(f"Temperature sensor {SENSOR_ID} not found")
        exit(1)

    sensor.change_resolution(resolution=Resolution.X0_25)
    return Decimal(str(sensor.get_temperature()))


if __name__ == "__main__":
    setup_gpio()

    temp = read_temperature()
    logger.info(f"Temperature: {temp}°C")

    if temp < TARGET_TEMP - HYSTERESIS:
        set_valve_mode(mode=MODE_HEAT)

    elif temp > TARGET_TEMP + HYSTERESIS:
        set_valve_mode(mode=MODE_COOL)

    GPIO.cleanup()
