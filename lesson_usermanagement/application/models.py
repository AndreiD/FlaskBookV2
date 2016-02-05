import datetime
from sqlalchemy import desc, or_, and_
from application import db
from flask.ext.security import SQLAlchemyUserDatastore, UserMixin, RoleMixin


roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    # __str__ is required by Flask-Admin, so we can have human-readable values for the Role when editing a User.
    # If we were using Python 2.7, this would be __unicode__ instead.
    def __str__(self):
        return self.name

    # __hash__ is required to avoid the exception TypeError: unhashable type: 'Role' when saving a User
    def __hash__(self):
        return hash(self.name)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    last_login_ip = db.Column(db.String(100))
    password = db.Column(db.String(255))
    current_login_ip = db.Column(db.String(100))
    login_count = db.Column(db.Integer)
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    # Required for administrative interface
    def __unicode__(self):
        return self.email

    def __repr__(self):
        return '<models.User[email=%s]>' % self.email

user_datastore = SQLAlchemyUserDatastore(db, User, Role)


class Tasks(db.Model):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(100))
    task = db.Column(db.String(255))
    at_time = db.Column(db.DateTime, default=datetime.datetime.now)
    user_ip = db.Column(db.String(46))
    user_agent = db.Column(db.String(100))

    def add_data(self, author, task, user_ip, user_agent):
        new_task = Tasks(author=author, task=task, user_ip=user_ip, user_agent=user_agent)
        db.session.add(new_task)
        db.session.commit()

    def list_all_tasks(self):
        return Tasks.query.all()

    def __repr__(self):
        return '<Task %r>' % (self.id)
