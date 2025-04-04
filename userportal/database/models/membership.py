import enum

from database.db import db

class MembershipTypes(enum.Enum):
    monthly = 1
    annually = 2
    def serialize(self):
        return {
            'id': self.value,
            'name': self.name
        }


class Membership(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    membership_type = db.Column(db.Enum(MembershipTypes) , nullable=False)
    active = db.Column(db.Boolean, nullable=False, default=True)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    has_used_free_trial = db.Column(db.Boolean, nullable=False,
                                    default=False)

    user = db.relationship('User', backref=db.backref('memberships', lazy=True))

    def serialize(self):

        return {
            'id': self.id,
            'membership_type': self.membership_type.name,  # Enum to string
            'active': self.active,
            'start_date': self.start_date.isoformat(),  # Date to string
            'end_date': self.end_date.isoformat(),  # Date to string
            'user_id': self.user_id,
            'has_used_free_trial': self.has_used_free_trial,
            'user': self.user.serialize() if self.user else None
        }
    def __repr__(self):
        return f'<Membership {self.membership_type} for User {self.user_id}>'