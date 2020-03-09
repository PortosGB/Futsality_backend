from flask import Blueprint, jsonify, request
from .models import User, Team, Booking, Notification
import jwt
import datetime
import sites.controllers.user_controller as UC
from .controllers import auth
router = Blueprint('router', __name__)


# first test route to check seeded data


@router.route('/')
def index():
    users = User.query.all()
    output = []
    for user in users:
        output.append(user.to_dict())
    teams = Team.query.all()
    for team in teams:
        output.append(team.to_dict())
    bookings = Booking.query.all()
    for booking in bookings:
        output.append(booking.to_dict())
    notifs = Notification.query.all()
    for n in notifs:
        output.append(n.to_dict())
    return jsonify({'users': output})


@router.route('/login', methods=['POST'])
def login():
    auth.authenticate(request)
