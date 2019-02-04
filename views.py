from random import randint

from flask import Blueprint

from forms import PaymentForm, PerformPaymentForm, ConfirmPaymentForm
from models import Invoice, db, Payment
from utils import send_response, send_code_confirm_payment_to_client, \
    get_payment_key

views = Blueprint('views', __name__)

from middleware import *


@views.route('/v1/invoices/<string:num>/balances', methods=['GET'])
def show_balance_invoice(num):
    invoice = Invoice.query.filter_by(num=num).first_or_404()
    return send_response(
        content={
            'message': 'ok',
            'balance': str(invoice.balance)
        },
        status_code=200
    )


@views.route('/v1/payments', methods=['POST'])
def create_payment():
    form = PaymentForm()
    if not form.validate_on_submit():
        return send_response(
            content=form.errors,
            status_code=400
        )

    if not is_exists_invoices(
        invoice_list=[
            form.number_invoice_provider.data,
            form.number_invoice_reciever.data
        ]
    ):
        return send_response(
            content={'message': 'Invoices does not exists'},
            status_code=404
        )

    key = get_payment_key()
    code_confirm = randint(100, 1000)
    db.session.add(
        Payment(
            key=key,
            amount_money=form.amount_money.data,
            number_invoice_provider=form.number_invoice_provider.data,
            number_invoice_reciever=form.number_invoice_reciever.data,
            code_confirm=code_confirm,
            status=Payment.NOT_CONFIRMED
        )
    )
    db.session.commit()
    send_code_confirm_payment_to_client(code=code_confirm)

    return send_response(
        content={'message': 'ok'},
        status_code=200
    )


def is_exists_invoices(invoice_list):
    invoices = Invoice.query.filter(Invoice.num.in_(invoice_list)).count()
    return invoices == len(invoice_list)


@views.route('/v1/payments/confirm', methods=['POST'])
def confirm_payment():
    form = ConfirmPaymentForm()
    if form.validate_on_submit():
        payment = Payment.query.filter_by(
            number_invoice_provider=form.invoice.data,
            code_confirm=form.code_confirm.data
        ).first_or_404()
        payment.status = Payment.CONFIRMED
        db.session.add(payment)
        db.session.commit()

        return send_response(
            content={
                'message': 'ok',
                'key': payment.key
            },
            status_code=200
        )
    return send_response(
        content=form.errors,
        status_code=400
    )


@views.route('/v1/payments/perform', methods=['POST'])
def perform_payment():
    form = PerformPaymentForm()
    if not form.validate_on_submit():
        return send_response(
            content=form.errors,
            status_code=400
        )

    payment = Payment.query.filter_by(key=form.key.data).first_or_404()
    if not payment.is_payment_available():
        return send_response(
            content={'message': 'Payment is not available'},
            status_code=400
        )

    provider, reciever = Invoice.query.filter(
        Invoice.num.in_(
            [
                payment.number_invoice_provider,
                payment.number_invoice_reciever
            ]
        )
    )
    provider.balance = provider.balance - payment.amount_money
    reciever.balance = reciever.balance + payment.amount_money
    payment.status = Payment.PERFORM
    db.session.add_all([provider, reciever, payment])
    db.session.commit()

    return send_response(
        content={'message': 'ok'},
        status_code=200
    )

