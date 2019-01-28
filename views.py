from random import randint

from flask import Blueprint

from forms import PaymentForm
from models import Invoice, db, Payment
from utils import send_response, send_code_confirm_payment_to_client, \
    get_payment_key

views = Blueprint('views', __name__)

from middleware import *


@views.route('/v1/invoices/<num>/balances', methods=['GET'])
def show_balance_invoice(num):
    try:
        invoice = Invoice.query.filter_by(num=num).first()
        return send_response(
            {
                'message': 'ok',
                'balance': str(invoice.balance)
            },
            200
        )
    except (KeyError, AttributeError):
        return send_response(
            {
                'message': 'Number invoice does not exists'
            },
            404
        )


@views.route('/v1/payments', methods=['POST'])
def create_payment():
    form = PaymentForm()
    if form.validate_on_submit():
        payment = request.get_json()

        if not is_exists_invoices(
            [
                payment['number_invoice_provider'],
                payment['number_invoice_reciever']
            ]
        ):
            return send_response(
                {
                    'message': 'Invoices does not exists'
                },
                404
            )

        key = get_payment_key()
        code_confirm = randint(100, 1000)

        db.session.add(
            Payment(
                key=key,
                amount_money=payment['amount_money'],
                number_invoice_provider=payment['number_invoice_provider'],
                number_invoice_reciever=payment['number_invoice_reciever'],
                code_confirm=code_confirm,
                status_id=1
            )
        )
        db.session.commit()

        send_code_confirm_payment_to_client(code_confirm)

        return send_response(
            {
                'message': 'ok'
            },
            200
        )

    return send_response(
        form.errors,
        400
    )


def is_exists_invoices(invoice_list):
    invoices = Invoice.query.filter(Invoice.num.in_(invoice_list)).all()
    return len(invoices) == len(invoice_list)


@views.route('/v1/payments/confirm', methods=['POST'])
def confirm_payment():
    req = request.get_json()

    payment = Payment.query.filter_by(
        number_invoice_provider=req['invoice'],
        code_confirm=req['code_confirm']
    ).scalar()

    if payment:
        return send_response(
            {
                'message': 'ok',
                'key': payment.key
            },
            200
        )

    return send_response(
        {
            'message': 'Invalid code'
        },
        400
    )
