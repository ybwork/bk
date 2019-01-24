from flask import jsonify


def send_json_response(message={}, status_code=200):
    response = jsonify(message)
    response.status_code = status_code
    return response


def send_payment_confirm_code_to_client(code):
    with open('payment_confirm_code.txt', 'w') as file:
        file.write(str(code))

