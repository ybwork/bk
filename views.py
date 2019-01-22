import os

from flask import Blueprint

from models import Bank, Client
from utils import send_json_response

views = Blueprint('views', __name__)

from middleware import *


@views.route('/balance', methods=['GET'])
def balance():
    # print(Client.query.with_parent(id))
    return send_json_response(
        message={'message': request.get_json()},
        status_code=200
    )
