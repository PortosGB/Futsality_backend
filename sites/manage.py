from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from .exts import db
from .models import User


app = Flask(__name__)
app.config.from_object('config')
db.init_app(app)



@app.route('/')
def index():
    users = User.query.all()

    output = []

    for user in users:
        user_data = {}
        user_data['firstname'] = user.firstname
        user_data['password'] = user.password
        user_data['admin'] = user.admin
        output.append(user_data)
    return jsonify({'users': output})

