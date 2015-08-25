import os
ROOT_PATH = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'mysql://pibot:P1B0t@192.168.1.2/pibot'
SQLALCHEMY_MIGRATE_REPO = os.path.join(ROOT_PATH, '../database')
