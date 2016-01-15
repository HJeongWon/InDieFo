from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from flask.ext.migrate import Migrate, MigrateCommand

db = SQLAlchemy()
migrate = Migrate()

class User(db.Model):
    """
    from test import db
    db.create_app()
    """
    __tablename__ = "user"

    idx = db.Column(db.Integer, primary_key=True)

    nickname = db.Column(db.String(20),unique=True)
    email = db.Column(db.String(20), unique=True)
    pw = db.Column(db.String(20))
    created = db.Column(db.DateTime, default=datetime.now)

    # no __init__()

class Comment(db.Model):
    __tablename__ = "comment"

    idx = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200))
    who = db.Column(db.Integer, db.ForeignKey('user.idx'))
class Board(db.Model):
    __tablename__ = "board"
    idx = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    num = db.Column(db.Integer(), default=0)
    count = db.Column(db.Integer(), default=0)
    good = db.Column(db.Integer(), default=0)
    bad = db.Column(db.Integer(), default=0)
    text = db.Column(db.String(10000))
    writer = db.Column(db.String(100))
    created = db.Column(db.DateTime, default=datetime.now)