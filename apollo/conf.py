import os
from decimal import Decimal

DATABASE_URL = os.getenv("DB_PATH", "postgresql://apollo:apollo@localhost/apollo")

DHT22_CHANNEL = 4

ONE_WIRE_SENSORS = {
    "RCT": {
        "address": "28000007162e15",
        "offset": Decimal(0.0),
    },
    "FLO": {
        "address": "28000007173569",
        "offset": Decimal(0.0),
    },
    "FHI": {
        "address": "280000071766e4",
        "offset": Decimal(0.0),
    },
    "CON": {
        "address": "28000007176e41",
        "offset": Decimal(0.0),
    },
    "STG": {
        "address": "28000007177269",
        "offset": Decimal(0.0),
    },
}

SATELLITES = {
    "IAM": {
        "location": "Hall",
        "temp_offset": Decimal(-5.1),
        "humidity_offset": Decimal(6.0),
    },
    "CX1": {
        "location": "Garage",
        "temp_offset": Decimal(-4.4),
        "humidity_offset": Decimal(8.0),
    },
    "CX2": {
        "location": "2nd floor",
        "temp_offset": Decimal(-6.1),
        "humidity_offset": Decimal(9.0),
    },
    "CX3": {
        "location": "Work room",
        "temp_offset": Decimal(-4.4),
        "humidity_offset": Decimal(8.0),
    },
    "CX4": {
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
