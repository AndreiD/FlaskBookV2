from application import app, logger, db
from flask import render_template, request, flash
from forms import *
from models import *


@app.route('/')
@app.route('/index')
def index():
    new_tasks = Tasks()
    new_tasks.add_data("Tom Hanks", "Clean the house please", request.remote_addr, request.headers.get('User-Agent'))

    list_records = Tasks().list_all_tasks()

    for record in list_records:
        logger.info(record.author + " " + record.task + " " + record.user_ip + " " + record.user_agent)

    return "see the console"


# Executes before the first request is processed.
@app.before_first_request
def before_first_request():
    logger.info("initializing the database >>>>>>>")
    db.create_all()
