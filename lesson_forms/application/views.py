from application import app, logger
from flask import render_template, request, flash
from forms import *


@app.route('/', methods=['GET', 'POST'])
def index():
    searchForm = SearchForm(request.form)

    if request.method == 'POST':
        if searchForm.validate():
            query_text = searchForm.tquery.data
            flash("You are searching with " + query_text, category="warning")
            return render_template("index.html", searchForm=searchForm)

    return render_template("index.html", searchForm=searchForm)


@app.route('/add_record', methods=['GET', 'POST'])
def add_record():
    form = Form_New_Message(request.form)

    if request.method == 'POST':
        if form.validate():
            logger.info("Processing new message.")

            logger.info(form.category.data + " " + form.title.data + " " + form.message.data + " " + form.author.data)

            flash("Your message was sent!", category="success")

    return render_template("add_record.html", form=form)
