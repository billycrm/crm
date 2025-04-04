from database.db import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    email_confirmed = db.Column(db.Boolean, nullable=False, default=False)
    user_confirmed = db.Column(db.Boolean, nullable=False, default=False)
    tokens = db.relationship('TokenList', backref='user', lazy=False, cascade='all, delete-orphan')

    admin = db.Column(db.Boolean, nullable=False, default=False)

    def serialize(self):
        return {
            'user_id': self.id,
            'username': self.username,
            'admin': self.admin,
            'email': self.email,
            'name': self.name,
            'email_confirmed': self.email_confirmed,
            'user_confirmed': self.user_confirmed,
            'membership_type': self.membership_type.name
        }

    def __repr__(self):
        return self.username + ' -- ' + self.email
