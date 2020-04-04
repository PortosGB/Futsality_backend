from flask import request, jsonify
from werkzeug.security import generate_password_hash
from sites.exts import db
from sites.models import User


# add other fields later
def create_user():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(
        email=data['email'],
        password=hashed_password,
        admin=False,
        firstname=data['firstname'],
        lastname=data['lastname'],
    )
    new_user.save()

    return jsonify({'message': 'New user created!'}), 201


def get(email):
    try:
        user = User.query.filter(User.email == email)[0]
        return jsonify({'user': user.to_dict()}), 200
    except IndexError:
        return jsonify({'error': 'User not found'}), 404


def get_many():
    users = User.query.all()
    output = []
    for user in users:
        output.append(user.to_dict())
    return jsonify({'users': output}), 200
