from random import randint

from flask import Blueprint

from forms import PaymentForm
from models import Invoice, db, Payment
from utils import send_json_response, send_code_confirm_payment_to_client, \
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
        return send_json_response(
            message={
                'balance': str(invoice.balance)
            },
            status_code=200
        )
    except (KeyError, AttributeError):
        return send_json_response(
            message={
                'error': 'Number invoice does not exists or invalid'
            },
            status_code=400
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

        send_code_confirm_payment_to_client(code_confirm)

        return send_json_response(
            message={'message': 'ok'},
            status_code=200
        )

    return send_json_response(
        message=form.errors,
        status_code=400
    )


@views.route('/v1/payments/confirm', methods=['POST'])
def confirm_payment():
    """
     http GET http://127.0.0.1:5000/v1/payments/confirm
     api_key=ccc42a8314596799 invoice=5956 code=372
    """
    confirm_params = request.get_json()

    payment = Payment.query.filter_by(
        invoice_provider=confirm_params['invoice'],
        code_confirm=confirm_params['code_confirm']
    ).scalar()

    if payment:
        return send_json_response(
            message={'key': payment.key},
            status_code=200
        )

    return send_json_response(
        message={'message': 'Invalid code'},
        status_code=400
    )
