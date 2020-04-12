from flask import Flask, jsonify
from .exts import db
from .urls import router
from flask_cors import CORS


def init_db():
    db.drop_all()
    db.create_all()


def register_extensions(_app):
    _app.register_blueprint(router)
    db.init_app(_app)


def create_app():
    _app = Flask(__name__)
    CORS(_app)
    _app.config.from_object('config')
    register_extensions(_app)
    return _app


app = create_app()
