import os
from decimal import Decimal

DATABASE_URL = os.getenv("DB_PATH", "postgresql://apollo:apollo@localhost/apollo")

SENSORS = {
    "reactor": {
        "address": "Hall",
        "offset": Decimal(0.0),
    },
    "coolant": {
        "address": "Garage",
        "offset": Decimal(0.0),
    },
    "storage": {
        "address": "",
        "offset": Decimal(0.0),
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
