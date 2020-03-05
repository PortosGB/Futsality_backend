from flask import Blueprint, jsonify
from .models import User

router = Blueprint('router', __name__)


# first test route

@router.route('/')
def index():
    users = User.query.all()
    output = []
    for user in users:
        output.append(user.to_dict())
    return jsonify({'users': output})
