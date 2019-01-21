import os

SECRET_KEY = os.urandom(16)
WTF_CSRF_ENABLED = False
SQLALCHEMY_DATABASE_URI = \
    'postgresql+psycopg2://user:pass@host:port/db_name'

from local_settings import *