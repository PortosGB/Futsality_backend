from flask import Blueprint, jsonify
from .models import User, Team, Booking

router = Blueprint('router', __name__)


# first test route

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
    return jsonify({'users': output})
