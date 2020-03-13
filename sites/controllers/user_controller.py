from flask import request, jsonify
from werkzeug.security import generate_password_hash
from sites.exts import db
from sites.models import User


# add other fields later
def create_user():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(email=data['email'], password=hashed_password, admin=False)
    new_user.save()

    return jsonify({'message': 'New user created!'}), 201
