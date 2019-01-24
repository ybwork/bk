from flask import Blueprint

from models import Invoice
from utils import send_json_response

views = Blueprint('views', __name__)

from middleware import *


@views.route('/invoice/<num>/balance', methods=['GET'])
def get(num):
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


@views.route('/payment_confirm_codes', methods=['POST'])
def create():
    return send_json_response(
        message='code',
        status_code=200
    )
