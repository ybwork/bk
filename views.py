import os

from flask import Blueprint

from utils import send_json_response

views = Blueprint('views', __name__)

# from middleware import *


@views.route('/', methods=['GET', 'POST'])
def home():
    return send_json_response(
        message={'message': os.urandom(16).hex()},
        status_code=200
    )
