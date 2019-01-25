import os

SECRET_KEY = ''
WTF_CSRF_ENABLED = True
SQLALCHEMY_DATABASE_URI = \
    'postgresql+psycopg2://user:pass@host:port/db_name'

from local_settings import *