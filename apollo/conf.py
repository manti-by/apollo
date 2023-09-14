import os

HELIOS_URL = "https://helios.manti.by"
HELIOS_USER = os.environ.get("HELIOS_USER")
HELIOS_PASS = os.environ.get("HELIOS_PASS")

DB_PATH = os.environ.get("DB_PATH", "/home/manti/data/db.sqlite")
TOKEN_PATH = os.environ.get("TOKEN_PATH", "/home/manti/data/token.txt")

DHT22_CHANNEL = 25

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
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "standard",
        },
        "filesystem": {
            "level": "WARNING",
            "class": "logging.FileHandler",
            "filename": os.environ.get("LOG_PATH", "/home/manti/logs/apollo.log"),
            "formatter": "standard",
        },
    },
    "loggers": {
        "": {"handlers": ["console", "filesystem"], "level": "DEBUG", "propagate": True}
    },
}
