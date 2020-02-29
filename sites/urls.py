from flask import Blueprint, jsonify
from .models import User

router = Blueprint('router', __name__)


@router.route('/')
def index():
    users = User.query.all()

    output = []

    for user in users:
        user_data = {}
        user_data['firstname'] = user.firstname
        user_data['last_name'] = user.firstname
        user_data['password'] = user.password
        user_data['admin'] = user.admin
        output.append(user_data)
    return jsonify({'users': output})
