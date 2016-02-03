from flask import Flask
import logging
app = Flask('application')
app.config.from_object('config.DevelopmentConfig')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)



import views