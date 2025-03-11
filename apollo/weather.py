import logging.config
from collections import defaultdict
from datetime import datetime, timedelta

import psycopg2
import requests
from psycopg2.extras import DictCursor

from apollo.conf import DATABASE_URL, LOGGING, MODE
from apollo.database import get_sensors_data, save_sensors_data, update_sensor_data


logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)

SENSOR_ID = "POGODA.BY"
API_URL = "https://pogoda.by/api/v2/numeric-weather/2/26852"


if __name__ == "__main__":
    connection = psycopg2.connect(DATABASE_URL, cursor_factory=DictCursor)

    data = requests.get(API_URL, timeout=60).json()
    for_date = next(iter(data))
    existing_dates = defaultdict(list)
    for x in get_sensors_data(connection, sensor_id=SENSOR_ID):
        existing_date = datetime.fromisoformat(x["context"]["DATES"]) + timedelta(
            hours=int(x["context"]["ADVANCE_TIME"])
        )
        existing_dates[existing_date].append(x)

    for item in data[for_date].values():
        temp = item["TMP"]
        created_at = datetime.fromisoformat(item["DATES"]) + timedelta(hours=int(item["ADVANCE_TIME"]))
        if created_at in existing_dates:
            data_is_updated = False
            for x in existing_dates[created_at]:
                if float(x["temp"]) != temp:
                    logger.warning(f"New temp value {temp} *C is received for {created_at}, old - {x['temp']} *C")
                    update_sensor_data(
                        connection=connection, record_id=x["id"], temp=temp, context={"mode": MODE, **item}
                    )
                    data_is_updated = True
            if not data_is_updated:
                logger.info(f"Skipping already existing {created_at} - {temp} *C")
                continue
        save_sensors_data(connection=connection, sensor_id=SENSOR_ID, temp=temp, context={"mode": MODE, **item})
        logger.info(f"{created_at} - {temp} *C")
