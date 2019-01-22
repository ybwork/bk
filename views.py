from flask import Blueprint

from models import Invoice
from utils import send_json_response

views = Blueprint('views', __name__)

from middleware import *


@views.route('/balance', methods=['GET'])
def balance():
    try:
        invoice = Invoice.query.filter_by(
            num=request.get_json()['number_invoice']
        ).first()
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
