.PHONY: apollo

define SENSORS_MIGRATION_SCRIPT
CREATE TABLE IF NOT EXISTS data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(32),
    temp INTEGER,
    humidity DECIMAL(5,2),
    datetime DATETIME DEFAULT CURRENT_TIMESTAMP
);
endef

export SENSORS_MIGRATION_SCRIPT
migrate:
	sqlite3 /home/manti/data/db.sqlite "$$SENSORS_MIGRATION_SCRIPT"

check:
	black apollo/
	flake8 apollo/
