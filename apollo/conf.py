import os
from decimal import Decimal

HELIOS_URL = "https://helios.manti.by"
HELIOS_USER = os.environ.get("HELIOS_USER")
HELIOS_PASS = os.environ.get("HELIOS_PASS")

DATABASE_URL = os.environ.get("DB_PATH", "postgresql://apollo:apollo@localhost/apollo")

TOKEN_PATH = os.environ.get("TOKEN_PATH", "/home/manti/data/token.txt")

DHT22_CHANNEL = 4

SENSORS = {
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
            "filename": "/home/manti/logs/app.log",
            "formatter": "standard",
        },
    },
    "loggers": {"": {"handlers": ["console", "file"], "level": "INFO", "propagate": True}},
}
