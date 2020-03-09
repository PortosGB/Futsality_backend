import jwt
import datetime
from flask import jsonify
from . import user_controller as uc
from ..models import User
from ..manage import app


def authenticate(request):
    username = request.json.get('username')
    password = request.json.get('password')
    user = User.query.filter_by(name=username).first()

    if uc.check_password_hash(password, password):
        token = jwt.encode(
            {'public_id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
            app.config['SECRET_KEY'])

    return jsonify({'token': token.decode('UTF-8')})
