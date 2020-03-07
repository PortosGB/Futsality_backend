from sqlalchemy.orm import relationship
from .exts import db
import datetime


class CRUD:
    def save(self):
        if self.id is None:
            db.session.add(self)
        return db.session.commit()

    def destroy(self):
        db.session.delete(self)
        return db.session.commit()


class User(db.Model, CRUD):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50))
    lastname = db.Column(db.String(50))
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    admin = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    last_connection = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    def to_dict(self):
        team = self.team.to_dict() if self.team else None
        return {
            'id': self.id,
            'firstname': self.firstname,
            'lastname': self.firstname,
            'password': self.password,
            'email': self.email,
            'admin': self.admin,
            'created_at': self.created_at,
            'last_connection': self.last_connection,
            'team': team
        }


class Team(db.Model, CRUD):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False, unique=True)
    # no foreign key here because of AmbiguousForeignKeysError, needs to be fixed later
    captain_id = db.Column(db.Integer, nullable=False, unique=True)
    players = db.relationship('User', backref="team")
    bookings = db.relationship('Booking', backref="team")

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'captain_id': self.captain_id,
            'players': [player.email for player in self.players]
        }


class Booking(db.Model, CRUD):
    id = db.Column(db.Integer, primary_key=True)
    side = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    booking_date = db.Column(db.Date, nullable=False)
    booking_start_hour = db.Column(db.String(6), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'created_at': self.created_at,
            'side': self.side,
            'booking_date': self.booking_date,
            'booking_start_hour': self.booking_start_hour,
            'team_id': self.team_id
        }


class Notification(db.Model, CRUD):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(10), nullable=False)
    answered = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    sender_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    recipient_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    sender = relationship("User", foreign_keys=[sender_id])
    recipient = relationship("User", foreign_keys=[recipient_id])

    def to_dict(self):
        return {
            'id': self.id,
            'created_at': self.created_at,
            'type': self.type,
            'sender': self.sender.email,
            'recipient': self.recipient.email,
            'answered': self.answered
        }
