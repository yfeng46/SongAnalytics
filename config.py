import os

DEBUG = True
LOGGING_CONFIG = "config/logging/local.conf"
PORT = 3000
APP_NAME = "song_analytics"

# local: export SQLALCHEMY_DATABASE_URI='sqlite:///song_analytics.db'
# rds: export SQLALCHEMY_DATABASE_URI="{conn_type}://{user}:{password}@{host}:{port}/{DATABASE_NAME}"

SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")

conn_type = "mysql+pymysql"
user = os.environ.get("MYSQL_USER")
password = os.environ.get("MYSQL_PASSWORD")
host = os.environ.get("MYSQL_HOST")
port = os.environ.get("MYSQL_PORT")
DATABASE_NAME = 'msia423'
SQLALCHEMY_DATABASE_URI =SQLALCHEMY_DATABASE_URI.format(conn_type=conn_type, user=user, password=password, host=host, port=port, DATABASE_NAME=DATABASE_NAME)


SQLALCHEMY_TRACK_MODIFICATIONS = True
HOST = "0.0.0.0"
MAX_ROWS_SHOW = 30
MODEL = "models/model.sav"

# # config for local
# DEBUG = True
# LOGGING_CONFIG = "config/logging/local.conf"
# PORT = 3002
# APP_NAME = "song_analytics"
# SQLALCHEMY_DATABASE_URI = 'sqlite:///song_analytics.db'
# SQLALCHEMY_TRACK_MODIFICATIONS = True
# HOST = "127.0.0.1"
# SQLALCHEMY_ECHO = False  # If true, SQL for queries made will be printed
# MAX_ROWS_SHOW = 100

# #config
# MODEL = "models/model.sav"
