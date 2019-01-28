from flask import request

from models import App
from utils import send_response
from views import views


@views.before_request
def exchange_format():
    if not request.is_json:
        return send_response(
            {
                'message': 'Not valid format data. Need JSON!'
            },
            400
        )


@views.before_request
def auth():
    try:
        api_key = request.get_json()['api_key']
    except KeyError:
        return send_response(
            {
                'message': 'Not sended api_key'
            },
            400
        )

    if not api_key:
        return send_response(
            {
                'message': 'Api key required'
            },
            401
        )

    if not is_valid_api_key(api_key=api_key):
        return send_response(
            {
                'message': 'Api key is not valid'
            },
            401
        )


def is_valid_api_key(api_key):
    if App.query.filter_by(key=api_key).scalar():
        return True
    return False

