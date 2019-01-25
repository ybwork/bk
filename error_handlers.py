from utils import send_json_response


def method_not_allowed(e):
    return send_json_response(
        message={'message': 'Method not allowed'},
        status_code=405
    )
