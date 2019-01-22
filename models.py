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


bank_client = db.Table(
    'bank_client',
    db.Column(
        'id',
        db.Integer,
        primary_key=True
    ),
    db.Column(
        'bank_id',
        db.Integer,
        db.ForeignKey('bank.id'),
        primary_key=True
    ),
    db.Column(
        'client_id',
        db.Integer,
        db.ForeignKey('client.id'),
        primary_key=True
    ),
    db.Column(
        'number_invoice',
        db.String(5),
        nullable=False
    ),
    db.Column(
        'balance',
        db.DECIMAL(10, 2),
        nullable=False
    )
)


class StatusOperation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)


class Operation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(5), nullable=False)
    amount_money = db.Column(db.DECIMAL(10, 2), nullable=False)
    number_invoice_provider = db.Column(db.String(5), nullable=False)
    number_invoice_reciever = db.Column(db.String(5), nullable=False)
    status_id = db.Column(
        db.Integer,
        db.ForeignKey('status_operation.id'),
        nullable=False
    )

