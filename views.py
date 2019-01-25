import json
from random import random, randint
from uuid import uuid4

from flask import Blueprint

from forms import PaymentForm
from models import Invoice, db, Payment
from utils import send_json_response, send_payment_confirm_code_to_client, \
    get_payment_key

views = Blueprint('views', __name__)

from middleware import *


@views.route('/v1/invoices/<num>/balances', methods=['GET'])
def show(num):
    """
     http GET http://127.0.0.1:5000/v1/invoices/5956f/balances
     api_key=ccc42a8314596799
    """
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


@views.route('/v1/payments', methods=['POST'])
def create_payment():
    """
    http POST http://127.0.0.1:5000/v1/payments
    api_key=ccc42a8314596799
    amount_money=300
    invoice_provider=5956
    invoice_reciever=5956
    """
    form = PaymentForm()

    if form.validate_on_submit():
        payment = request.get_json()
        key = get_payment_key()
        code_confirm = randint(100, 1000)

        db.session.add(
            Payment(
                key=key,
                amount_money=payment['amount_money'],
                invoice_provider=payment['invoice_provider'],
                invoice_reciever=payment['invoice_reciever'],
                code_confirm=code_confirm,
                status_id=1
            )
        )
        db.session.commit()

        send_payment_confirm_code_to_client(code_confirm)

        message = {'message': 'ok'}
        status_code = 400
    else:
        message = form.errors
        status_code = 400

    return send_json_response(
        message=message,
        status_code=status_code
    )


@views.route('/v1/payment_confirm_codes/check', methods=['POST'])
def check():
    """
     http GET http://127.0.0.1:5000/v1/payment_confirm_codes/check
     api_key=ccc42a8314596799 code=152
    """
    pass
