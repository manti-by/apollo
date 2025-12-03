import configparser
import os
from pathlib import Path

from apollo.services.models import Sensor


BASE_DIR = Path(__file__).resolve().parent.parent

config = configparser.ConfigParser()
config.read(BASE_DIR / "settings.ini")

MODE = os.getenv("MODE", config["default"]["mode"])
IS_SHINE = MODE == "shine"

DATABASE_URL = os.getenv("DB_PATH", config["database"]["url"])

SENSORS = {
    "T1": Sensor(sensor_id="28000007176e41", label_shine="CONNECT", label_warm="RADI-RS", context={"mode": MODE}),
    "T2": Sensor(sensor_id="28000007162e15", label_shine="REACTOR", label_warm="WF-1-IN", context={"mode": MODE}),
    "T3": Sensor(sensor_id="28000007173569", label_shine="FRZR-LO", label_warm="WF-1-OU", context={"mode": MODE}),
    "T4": Sensor(sensor_id="280000071766e4", label_shine="FRZR-HI", label_warm="WF-2-IN", context={"mode": MODE}),
    "T5": Sensor(sensor_id="28000007177269", label_shine="STORAGE", label_warm="WF-2-OU", context={"mode": MODE}),
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
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
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": os.getenv("LOG_PATH", config["logging"]["path"]),
            "formatter": "standard",
        },
    },
    "loggers": {"": {"handlers": ["console", "file"], "level": "INFO", "propagate": True}},
}
