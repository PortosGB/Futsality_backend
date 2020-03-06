# This file will contains all the seeds for the DB, the seed_db method is launched by the cli.command("init_db")
from .exts import db
import logging as lg
from .models import User, Team


def seed_db():
    seed_users()
    db.session.commit()
    lg.warning('DB INITIALIZED !')


def seed_users():
    user_a = User(email="test@test.fr", firstname='Alex', lastname='Dupont',
                  admin=False, password="passsword")
    user_b = User(email="test2@test.fr", firstname='Michel', lastname='Dupont',
                  admin=False, password="passsword")
    user_a.save()
    user_b.save()
    seed_teams(user_a, user_b)


def seed_teams(user_a, user_b):
    team_a = Team(name='Juventus', captain_id=user_a.id)
    team_a.save()
    user_a.team_id = team_a.id
    user_a.save()
    user_b.team_id = team_a.id
    user_b.save()
