from flask import Blueprint, jsonify, request
from flask_cors import cross_origin

from .models import User, Team, Booking, Notification
import jwt
from flask import current_app as app
from functools import wraps
import datetime
import sites.controllers.user_controller as uc
import sites.controllers.notification_controller as nc
from .controllers import auth

router = Blueprint('router', __name__)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query.filter_by(id=data['id']).first()
        except Exception as e:
            return jsonify({'message': 'Token is invalid!'}), 401
        return f(current_user, *args, **kwargs)

    return decorated


# first test route to check seeded data


@router.route('/')
# @token_required
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
    return auth.authenticate()


'''
    USERS MANAGEMENT
'''


@router.route('/user', methods=['POST'])
def create_user():
    return uc.create_user()


@router.route('/user/', methods=['GET'])
@token_required
def get_user(current_user):
    id = request.args.get('id')
    if id:
        return uc.get(id)
    return uc.get_many()


@router.route('/user/<int:id>', methods=['DELETE'])
@token_required
def delete_user(current_user, id):
    return uc.delete(current_user, id)


@router.route('/user/<int:id>', methods=['PATCH'])
@token_required
def update_user(current_user, id):
    return uc.update(current_user, id)


@router.route('/current_user', methods=['GET'])
@token_required
def current_user(current_user):
    return jsonify({'user': current_user.to_dict()}), 200


'''
    NOTIFICATIONS MANAGEMENT
'''

@router.route('/notification', methods=['POST'])
@token_required
def create_notification(current_user):
    return nc.create(current_user)