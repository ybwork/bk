from uuid import uuid4

from flask import jsonify


def send_response(content, status_code):
    response = jsonify(content)
    response.status_code = status_code
    return response


def send_code_confirm_payment_to_client(code):
    with open('code_confirm_payment.txt', 'w') as file:
        file.write(str(code))


def get_payment_key():
    return str(uuid4())[:5]

