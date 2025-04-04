import enum

from database.db import db

class MembershipTypes(enum.Enum):
    monthly = 1
    annually = 2


class Membership(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    membership_type = db.Column(db.Enum(MembershipTypes) , nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    has_used_free_trial = db.Column(db.Boolean, nullable=False,
                                    default=False)

    user = db.relationship('User', backref=db.backref('memberships', lazy=True))

    def __repr__(self):
        return f'<Membership {self.membership_type} for User {self.user_id}>'