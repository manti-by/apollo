.PHONY: apollo

define SENSORS_MIGRATION_SCRIPT
CREATE TABLE IF NOT EXISTS data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    temp INTEGER,
    humidity DECIMAL(5,2),
    moisture DECIMAL(5,2),
    luminosity DECIMAL(5,2),
    datetime DATETIME DEFAULT CURRENT_TIMESTAMP
);
endef

export SENSORS_MIGRATION_SCRIPT
migrate:
	sqlite3 /home/manti/www/apollo/data/db.sqlite "$$SENSORS_MIGRATION_SCRIPT"

check:
	black apollo/
	flake8 apollo/
