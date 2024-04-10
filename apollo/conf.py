import os
from decimal import Decimal

DATABASE_URL = os.getenv("DB_PATH", "postgresql://apollo:apollo@localhost/apollo")

SENSORS = {
    "REACTOR": {
        "address": "28000007162e15",
        "offset": Decimal(0.0),
    },
    "FRZR-LO": {
        "address": "28000007173569",
        "offset": Decimal(0.0),
    },
    "FRZR-HI": {
        "address": "280000071766e4",
        "offset": Decimal(0.0),
    },
    "CONNECT": {
        "address": "28000007176e41",
        "offset": Decimal(0.0),
    },
    "STORAGE": {
        "address": "28000007177269",
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
