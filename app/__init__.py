import os
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from logging.handlers import RotatingFileHandler


app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)


if not app.debug:  # and app.testing
    # logging to file
    log_dir = app.config['LOG_DIR']
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)
    file_handler = RotatingFileHandler(os.path.join(log_dir, 'cas-mockup.log'), maxBytes=10240,
                                       backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('CAS startup')

from app import routes, models
