from random import random, randint

from flask import Blueprint

from models import Invoice, db
from utils import send_json_response

views = Blueprint('views', __name__)

from middleware import *


@views.route('/v1/invoices/<num>/balances', methods=['GET'])
def show(num):
    try:
        invoice = Invoice.query.filter_by(num=num).first()
        message = {
            'balance': str(invoice.balance)
        }
        status_code=200
    except (KeyError, AttributeError):
        message = {
            'error': 'Number invoice does not exists or invalid'
        }
        status_code = 400

    return send_json_response(
        message=message,
        status_code=status_code
    )


@views.route('/v1/payment_confirm_codes', methods=['POST'])
def create():
    try:
        # взять пользователя по счёту
        invoice = Invoice.query.filter_by(
            num=request.get_json()['invoice']
        ).first()

        # сгенерить код
        payment_confirm_code = randint(100, 1000)

        # записать код в базу
        invoice.client.payment_confirm_code = payment_confirm_code
        db.session.add(invoice.client)
        db.session.commit()

        # отправить код на почту (сейчас в файл)
        with open('email.txt', 'w') as file:
            file.write(str(payment_confirm_code))

        message = {
            'message': 'ok'
        }
        status_code=200
    except(KeyError, ValueError):
        message = {
            'error': 'Number invoice does not exists or invalid'
        }
        status_code = 400

    return send_json_response(
        message=message,
        status_code=status_code
    )

