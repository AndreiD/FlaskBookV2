from flask import Flask
import logging
from flask.ext.sqlalchemy import SQLAlchemy
from flask_mail import Mail

app = Flask('application')
app.config.from_object('config.DevelopmentConfig')

db = SQLAlchemy(app)


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


mail = Mail(app)

import views, models
