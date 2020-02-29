from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from .exts import db
from .models import User
from .urls import router


def register_extensions(_app):
    _app.register_blueprint(router)
    db.init_app(_app)


def create_app():
    _app = Flask(__name__)
    _app.config.from_object('config')
    register_extensions(_app)
    return _app


app = create_app()
