import logging

import psycopg2
from flask import Flask
from flask_cors import CORS
from flask_mail import Mail
# from flask_socketio import SocketIO
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
app.logger.setLevel(logging.INFO)

db = psycopg2.connect(app.config['DATABASE_URI'])
cors = CORS(app, resources={r"/*": {"origins": "*"}})
mail = Mail(app)
# socketio = SocketIO(app, async_mode=app.config['SOCKETIO_ASYNC_MODE'])

from admin import admin   # noqa # isort:skip
from authentication import routes     # noqa # isort:skip
from bulkupload import bulkupload           # noqa # isort:skip

app.register_blueprint(admin)
app.register_blueprint(routes)
app.register_blueprint(bulkupload)