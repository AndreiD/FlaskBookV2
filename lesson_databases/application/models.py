import datetime
from application import db


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
