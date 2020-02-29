import logging as lg

from .exts import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50))
    lastname = db.Column(db.String(50))
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(255), unique=True)
    admin = db.Column(db.Boolean)


def seed_db():
    db.session.add(User(email="test@test.fr", firstname='Alex', lastname='Dupont', admin=False, password="passsword"))
    db.session.commit()
    lg.warning('DB INITIALISZED')
