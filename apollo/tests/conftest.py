from urllib.parse import urlparse, urlunparse

import psycopg2
import pytest
from psycopg2.extras import DictCursor

from ..settings import BASE_DIR, DATABASE_URL


@pytest.fixture(scope="session", autouse=True)
def db_connection():
    """This fixture will be executed once, creating the given database and table."""
    database_url = urlparse(DATABASE_URL)
    test_database_name = f"{database_url.path}_test"
    database_url = database_url._replace(path=test_database_name)
    test_database_name = test_database_name.lstrip("/")
    test_database_url = str(urlunparse(database_url))

    connection = psycopg2.connect(DATABASE_URL, cursor_factory=DictCursor)
    connection.autocommit = True
    try:
        connection.cursor().execute(f"CREATE DATABASE {test_database_name}")
    except psycopg2.errors.DuplicateDatabase:
        pass
    connection.close()

    connection = psycopg2.connect(test_database_url, cursor_factory=DictCursor)
    connection.autocommit = True

    try:
        with open(BASE_DIR / "utils" / "create_database.sql") as f:
            create_table_query = f.read()
        connection.cursor().execute(create_table_query)
    except psycopg2.errors.DuplicateTable:
        pass

    try:
        connection.cursor().execute("CREATE INDEX created_at_index ON data (created_at DESC)")
    except psycopg2.errors.DuplicateTable:
        pass
    yield connection


@pytest.fixture(scope="function", autouse=True)
def clear_tables(db_connection):
    """This fixture will be executed after every test, clearing the given table."""
    yield
    db_connection.cursor().execute("TRUNCATE TABLE data RESTART IDENTITY;")
