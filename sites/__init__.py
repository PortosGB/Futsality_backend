from flask import Flask

from .manage import app
from . import models
from . import seeds


@app.cli.command("init_db")
def init_db():
    manage.init_db()
    seeds.seed_db()
