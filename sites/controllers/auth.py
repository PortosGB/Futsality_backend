import jwt
import datetime
from flask import jsonify, request
from flask import current_app as app
from werkzeug.security import check_password_hash

from ..models import User


def auth_error(status_code, message):
    response = jsonify({
        'status': status_code,
        'message': message,
    })
    response.status_code = status_code
    return response


def authenticate():
    email = request.args.get('email')
    password = request.args.get('password')
    user = User.query.filter_by(email=email).first()
    if not user:
        return auth_error(401, 'Unauthorized')
    if not check_password_hash(user.password, password):
        return auth_error(401, 'Unauthorized')
    token = jwt.encode(
        {'id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
        app.config['SECRET_KEY'])

    return jsonify({'token': token.decode('UTF-8')})


# def login():
#     token = jwt.encode(
#         {'public_id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
#         app.config['SECRET_KEY'])
#
#     return jsonify({'token': token.decode('UTF-8')})
