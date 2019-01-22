from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table

db = SQLAlchemy()


class App(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    key = db.Column(db.String(16), unique=True, nullable=False)


class Bank(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    balance = db.Column(db.DECIMAL(10, 2), nullable=False)


class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), nullable=False)

