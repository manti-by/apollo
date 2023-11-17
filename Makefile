.PHONY: apollo

define SENSORS_MIGRATION_SCRIPT
CREATE TABLE IF NOT EXISTS data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sensor_id VARCHAR(32),
    temp DECIMAL(5,2),
    humidity DECIMAL(5,2),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
endef

export SENSORS_MIGRATION_SCRIPT
migrate:
	sqlite3 db.sqlite "$$SENSORS_MIGRATION_SCRIPT"

check:
	black apollo/
	flake8 apollo/
