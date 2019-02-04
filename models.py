from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class App(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    key = db.Column(db.String(16), unique=True, nullable=False)


class Bank(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    balance = db.Column(db.DECIMAL(10, 2), nullable=False)
    invoices = db.relationship('Invoice', backref='invoice', lazy=True)


class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    invoice = db.relationship('Invoice', backref='client', lazy=True)


class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    num = db.Column(db.String(5), nullable=False)
    balance = db.Column(db.DECIMAL(10, 2), nullable=False)
    bank_id = db.Column(db.Integer, db.ForeignKey('bank.id'), nullable=False)
    client_id = db.Column(
        db.Integer,
        db.ForeignKey('client.id'),
        nullable=False
    )


class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(5), nullable=False)
    amount_money = db.Column(db.DECIMAL(10, 2), nullable=False)
    number_invoice_provider = db.Column(db.String(5), index=True, nullable=False)
    number_invoice_reciever = db.Column(db.String(5), nullable=False)
    code_confirm = db.Column(db.Integer, index=True, nullable=True)

    NOT_CONFIRMED = 'не подтвержден'
    CONFIRMED = 'подтвержден'
    PERFORM = 'выполнен'
    CANCELED = 'отменен'
    status = db.Column(
        db.String(255),
        nullable=False,
        index=True
    )

    def is_payment_available(self):
        return self.status == self.CONFIRMED
