import configparser
import os
from decimal import Decimal


config = configparser.ConfigParser()
config.read("settings.ini")

MODE = os.getenv("MODE", config["default"]["mode"])

DATABASE_URL = os.getenv("DB_PATH", config["database"]["url"])

DHT22_CHANNEL = 4

ONE_WIRE_SENSORS = {
    "REACTOR": {
        "address": "28000007162e15",
        "temp_offset": Decimal(0.0),
    },
    "FRZR-LO": {
        "address": "28000007173569",
        "temp_offset": Decimal(0.0),
    },
    "FRZR-HI": {
        "address": "280000071766e4",
        "temp_offset": Decimal(0.0),
    },
    "CONNECT": {
        "address": "28000007176e41",
        "temp_offset": Decimal(0.0),
    },
    "STORAGE": {
        "address": "28000007177269",
        "temp_offset": Decimal(0.0),
    },
}

SATELLITES = {
    "CORUSCANT": {
        "location": "Hall",
        "temp_offset": Decimal(-5.1),
        "humidity_offset": Decimal(6.0),
    },
    "CENTAX-1": {
        "location": "Garage",
        "temp_offset": Decimal(-4.4),
        "humidity_offset": Decimal(8.0),
    },
    "CENTAX-2": {
        "location": "2nd floor",
        "temp_offset": Decimal(-6.1),
        "humidity_offset": Decimal(9.0),
    },
    "CENTAX-3": {
        "location": "Work room",
        "temp_offset": Decimal(-4.4),
        "humidity_offset": Decimal(8.0),
    },
    "CENTAX-4": {
        "location": "Bedroom",
        "temp_offset": Decimal(-6.1),
        "humidity_offset": Decimal(9.0),
    },
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "standard": {
            "format": "%(asctime)s %(levelname)-8s %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        }
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "standard",
        },
        "file": {
            "level": "WARNING",
            "class": "logging.FileHandler",
            "filename": os.getenv("LOG_PATH", config["logging"]["path"]),
            "formatter": "standard",
        },
    },
    "loggers": {"": {"handlers": ["console", "file"], "level": "INFO", "propagate": True}},
}
