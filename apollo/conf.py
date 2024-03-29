import os

HELIOS_URL = "https://helios.manti.by"
HELIOS_USER = os.environ.get("HELIOS_USER")
HELIOS_PASS = os.environ.get("HELIOS_PASS")

DB_PATH = os.environ.get("DB_PATH", "/home/manti/www/apollo/data/db.sqlite")
PHOTO_PATH = os.environ.get("PHOTO_PATH", "/home/manti/www/apollo/data/photo/")
TOKEN_PATH = os.environ.get("TOKEN_PATH", "/home/manti/www/apollo/data/token.txt")

SPI_PORT = 0
SPI_DEVICE = 0

DHT22_CHANNEL = 25

SMS_CHANNEL = 1
SMS_LOW = 1.12148
SMS_HIGH = 2.78438

LMS_CHANNEL = 0
LMS_LOW = 0.07077
LMS_HIGH = 2.96163

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
            "filename": os.environ.get("LOG_PATH", "/home/manti/www/apollo/logs/apollo.log"),
            "formatter": "standard",
        },
    },
    "loggers": {
        "": {"handlers": ["console", "filesystem"], "level": "DEBUG", "propagate": True}
    },
}
