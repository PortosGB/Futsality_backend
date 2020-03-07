# This file will contains all the seeds for the DB, the seed_db method is launched by the cli.command("init_db")
# TODO refactor this file
import logging as lg
import datetime
from .exts import db
from .models import User, Team, Booking, Notification


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
    seed_bookings(team_a)
    seed_notif(user_a, user_b)


def seed_bookings(team_a):
    booking_a = Booking(side=1, booking_date=datetime.date(2020, 3, 13), booking_start_hour="15:00", team_id=team_a.id)
    booking_a.save()


def seed_notif(user_a, user_b):
    notif_a = Notification(sender=user_a, recipient=user_b, type="invitation")
    notif_a.save()
