from enum import unique
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
import hashlib
from flask import request

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(300), unique=True)
    icNumber = db.Column(db.Integer, unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
 



