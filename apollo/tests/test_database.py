from datetime import UTC, datetime
from decimal import Decimal

from apollo.services.database import (
    get_not_synced_sensors_data,
    get_sensors_data,
    save_sensors_data,
    update_sensor_data,
)


class TestDatabase:
    def test_create_and_get_sensors(self, db_connection):
        temp = Decimal("20.5")
        sensors = get_sensors_data(connection=db_connection)
        assert len(sensors) == 0

        for i in range(3):
            save_sensors_data(connection=db_connection, sensor_id=f"test {i}", temp=temp)

        sensors = get_sensors_data(connection=db_connection)
        assert len(sensors) == 3

    def test_create_and_update_sensor(self, db_connection):
        temp = Decimal("20.5")
        save_sensors_data(connection=db_connection, sensor_id="test", temp=temp)
        sensors = get_sensors_data(connection=db_connection)
        assert len(sensors) == 1

        record_id = sensors[0]["id"]
        update_sensor_data(connection=db_connection, record_id=record_id, temp=temp)
        sensors = get_sensors_data(connection=db_connection)
        assert sensors[0]["temp"] == temp

        update_sensor_data(connection=db_connection, record_id=record_id, temp=temp, context={"test": "test"})
        sensors = get_sensors_data(connection=db_connection)
        assert sensors[0]["context"] == {"test": "test"}
        assert not sensors[0]["synced_at"]

        update_sensor_data(connection=db_connection, record_id=record_id, temp=temp, synced_at=datetime.now(UTC))
        sensors = get_sensors_data(connection=db_connection)
        assert sensors[0]["synced_at"]

    def test_not_synced_sensors(self, db_connection):
        temp = Decimal("20.5")
        save_sensors_data(connection=db_connection, sensor_id="test 1", temp=temp)
        save_sensors_data(connection=db_connection, sensor_id="test 2", temp=temp)
        sensors = get_sensors_data(connection=db_connection)

        record_id = sensors[0]["id"]
        update_sensor_data(connection=db_connection, record_id=record_id, temp=temp, synced_at=datetime.now(UTC))

        all_sensors = get_sensors_data(connection=db_connection)
        assert len(all_sensors) == 2

        not_synced_sensors = get_not_synced_sensors_data(connection=db_connection)
        assert len(not_synced_sensors) == 1
