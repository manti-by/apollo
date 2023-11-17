from __future__ import annotations

import logging.config
import os

import requests

from apollo.conf import HELIOS_PASS, HELIOS_URL, HELIOS_USER, LOGGING, TOKEN_PATH
from apollo.database import get_sensors_data

logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)


def get_token() -> str | None:
    if os.path.exists(TOKEN_PATH):
        with open(TOKEN_PATH, "r") as f:
            return f.read()
    response = requests.post(
        f"{HELIOS_URL}/api/v1/users/login/",
        json={"email": HELIOS_USER, "password": HELIOS_PASS},
        headers={"Content-Type": "application/json"},
    )
    logger.debug(response.reason)
    if response.ok:
        token = response.json().get("token")
        with open(TOKEN_PATH, "w") as f:
            f.write(token)
        return token


def send_data(token: str, data: list[dict]) -> bool:
    response = requests.post(
        f"{HELIOS_URL}/api/v1/sensors/",
        json=data,
        headers={"Content-Type": "application/json", "Authorization": f"Token {token}"},
    )
    logger.debug(response.reason)
    return response.ok


if __name__ == "__main__":
    if not (auth_token := get_token()):
        logger.error("Can't retrieve token, check credentials")
        exit(-1)

    if not (sensors_data := get_sensors_data()):
        logger.error("Can't get data from database")
        exit(-1)

    if not send_data(auth_token, sensors_data):
        logger.error("Error sending sensors data")
        exit(-1)

    logger.info("Data is successfully sent")
