from flask import request

from forms import AuthForm
from models import App
from utils import send_json_response
from views import views


@views.before_request
def exchange_format():
    if not request.is_json:
        return send_json_response(
            message={
                'message': 'Not valid format data. Need JSON!'
            },
            status_code=400
        )


@views.before_request
def auth():
    try:
        api_key = request.get_json()['api_key']
    except KeyError:
        return send_json_response(
            message='Not sended api_key',
            status_code=400
        )

    if not api_key:
        return send_json_response(
            message={'message': 'Api key required'},
            status_code=401
        )

    if not is_valid_api_key(api_key=api_key):
        return send_json_response(
            message={'message': 'Api key is not valid'},
            status_code=401
        )


def is_valid_api_key(api_key):
    if App.query.filter_by(key=api_key).scalar():
        return True
    return False

