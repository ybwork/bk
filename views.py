from random import randint

from flask import Blueprint

from forms import PaymentForm, PaymentPerformForm
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
            content={
                'message': 'ok',
                'balance': str(invoice.balance)
            },
            status_code=200
        )
    except (KeyError, AttributeError):
        return send_response(
            content={'message': 'Number invoice does not exists'},
            status_code=404
        )


@views.route('/v1/payments', methods=['POST'])
def create_payment():
    form = PaymentForm()
    if form.validate_on_submit():
        payment = request.get_json()

        if not is_exists_invoices(
            invoice_list=[
                payment['number_invoice_provider'],
                payment['number_invoice_reciever']
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
                amount_money=payment['amount_money'],
                number_invoice_provider=payment['number_invoice_provider'],
                number_invoice_reciever=payment['number_invoice_reciever'],
                code_confirm=code_confirm,
                status_id=1
            )
        )
        db.session.commit()

        send_code_confirm_payment_to_client(code=code_confirm)

        return send_response(
            content={'message': 'ok'},
            status_code=200
        )

    return send_response(
        content=form.errors,
        status_code=400
    )


def is_exists_invoices(invoice_list):
    invoices = Invoice.query.filter(Invoice.num.in_(invoice_list)).count()
    return invoices == len(invoice_list)


@views.route('/v1/payments/confirm', methods=['POST'])
def confirm_payment():
    req = request.get_json()

    payment = Payment.query.filter_by(
        number_invoice_provider=req['invoice'],
        code_confirm=req['code_confirm']
    ).scalar()

    if payment:
        # меняем статус платежа на подтвержден

        return send_response(
            content={
                'message': 'ok',
                'key': payment.key
            },
            status_code=200
        )

    return send_response(
        content={'message': 'Invalid code'},
        status_code=400
    )


@views.route('/v1/payments/perform', methods=['POST'])
def perform_payment():
    form = PaymentPerformForm()
    if form.validate_on_submit():
        # берем из таблицы payment номер счетов по ключу операции
        # payment = Payment.query.filter_by(key=request.key)

        # идем в таблицу invoice и переводим со счета
        # number_invoice_provider на счет number_invoice_reciever

        # идем в таблицу payment и меняем статус платежа на завершен
        return send_response(
            content={'message': 'ok'},
            status_code=200
        )
    return send_response(
        content=form.errors,
        status_code=400
    )
