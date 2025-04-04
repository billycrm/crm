from database.db import db
import datetime


class Logs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    action = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, user_id, action, url):
        self.user_id = user_id
        self.action = action
        self.url = url
        self.created_at = datetime.datetime.now()
