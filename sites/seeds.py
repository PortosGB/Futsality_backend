# This file will contains all the seeds for the DB, the seed_db method is launched by the cli.command("init_db")
from .exts import db
import logging as lg
from .models import User


def seed_db():
    seed_users()
    db.session.commit()
    lg.warning('DB INITIALIZED !')


def seed_users():
    db.session.add(User(email="test@test.fr", firstname='Alex', lastname='Dupont',
                        admin=False, password="passsword"))
    db.session.add(User(email="test2@test.fr", firstname='Michel', lastname='Dupont',
                        admin=False, password="passsword"))
