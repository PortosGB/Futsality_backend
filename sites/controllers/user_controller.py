from flask import request, jsonify
from werkzeug.security import generate_password_hash
from sites.exts import db
from sites.models import User


def update_user_attributes(user, data):
    for key, value in data.items():
        if str(key) == "password":
            hashed_password = generate_password_hash(value, method='sha256')
            user.password = hashed_password
        elif hasattr(user, str(key)):
            setattr(user, str(key), value)
    user.save()


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


def get(id):
    user = User.query.get(id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify({'user': user.to_dict()}), 200


def get_many():
    users = User.query.all()
    output = []
    for user in users:
        output.append(user.to_dict())
    return jsonify({'users': output}), 200


def delete(current_user, id):
    user = User.query.get(id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    if current_user.id != id and (not current_user.admin):
        return jsonify({'message': 'Unauthorized'}), 403
    user.destroy()
    return jsonify({'message': 'User successfully deleted'}), 200


def update(current_user, id):
    user = User.query.get(id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    if current_user.id != id and (not current_user.admin):
        return jsonify({'message': 'Unauthorized'}), 403
    data = request.get_json()
    update_user_attributes(user, data)
    return jsonify({'message': 'User successfully updated'}), 200
