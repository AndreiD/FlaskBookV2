from flask import request, render_template, flash, current_app, jsonify, Config, redirect

from application import app, logger, db
from flask.ext.security import Security, login_required, logout_user, current_user, utils
from flask.ext.security.utils import verify_password
from flask_admin import Admin, base, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from application.models import *
import logging
import requests
from models import *
import json
import urllib

security = Security(app, user_datastore)


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")


@app.route('/secret')
@login_required
def secret():
    return render_template("secret.html")


@app.before_first_request
def before_first_request():
    logging.info("-------------------- initializing everything ---------------------")
    db.create_all()

    user_datastore.find_or_create_role(name='admin', description='Administrator')
    user_datastore.find_or_create_role(name='editor', description='Editor')
    user_datastore.find_or_create_role(name='enduser', description='End-User')

    encrypted_password = utils.encrypt_password('hardpassword')
    if not user_datastore.get_user('admin@admin.com'):
        user_datastore.create_user(email='admin@admin.com', password=encrypted_password, active=True,
                                   confirmed_at=datetime.datetime.now())

    encrypted_password = utils.encrypt_password('editorpassword')
    if not user_datastore.get_user('editor@editor.com'):
        user_datastore.create_user(email='editor@editor.com', password=encrypted_password, active=True,
                                   confirmed_at=datetime.datetime.now())

    db.session.commit()

    user_datastore.add_role_to_user('admin@admin.com', 'admin')
    user_datastore.add_role_to_user('editor@editor.com', 'editor')
    db.session.commit()


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500




# -------------------------- ADMIN PART ------------------------------------

# required by admin.
@app.route('/logout')
def logout():
    logout_user()
    return redirect(request.args.get('next') or '/')

class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.has_role('admin')


# ------- visible only to admin user, else returns "not found" -----------
class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if not current_user.has_role('admin'):
            flash("You must be admin in order to access the admin panel", category="danger")
            return redirect("/")
        return self.render('admin/index.html')


class ExpenseAdminView(MyModelView):
    can_create = True

    def is_accessible(self):
        return current_user.has_role('admin')

    def __init__(self, session, **kwargs):
        super(ExpenseAdminView, self).__init__(Tasks, session, **kwargs)


class UserAdminView(MyModelView):
    column_exclude_list = ('password')

    def is_accessible(self):
        return current_user.has_role('admin')

    def __init__(self, session, **kwargs):
        super(UserAdminView, self).__init__(User, session, **kwargs)


class RoleView(MyModelView):
    def is_accessible(self):
        return current_user.has_role('admin')

    def __init__(self, session, **kwargs):
        super(RoleView, self).__init__(Role, session, **kwargs)


admin = Admin(app, name='Hive Admin', index_view=MyAdminIndexView(), template_mode='bootstrap3')
admin.add_view(ExpenseAdminView(db.session))
admin.add_view(UserAdminView(db.session))
admin.add_view(RoleView(db.session))
admin.add_link(base.MenuLink('Web Home', endpoint="index"))
admin.add_link(base.MenuLink('Logout', endpoint="logout"))

# --------------------------  END ADMIN PART ---------------------------------