import os


class Config(object):
    APP_ROOT = os.path.dirname(os.path.abspath(__file__))
    FLASK_APP = 'app_runner.py'
    FLASK_ENV = 'development'
    FLASK_APP_PORT = 5000
    FILE_URL = 'http://localhost:5000/'
    FLASK_APP_HOST = '127.0.0.1'
    FLASK_DEBUG = 1
    SECRET_KEY = 'fdhfjkjhfdsfiuhfifhoud3247348938@i3943789ddh'
    MAIL_SERVER_TYPE = 'local'
    MAIL_SENDER = 'Administrator'
    # MAIL_RECEIVERS = ['']
    MAIL_RECEIVERS = []
    MAIL_DOMAIN_TYPE = 'http://localhost:4200/#/'
    DATABASE_URI = 'postgresql://postgres:postgres@localhost/testdb'