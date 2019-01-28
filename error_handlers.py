from utils import send_response


def method_not_allowed(e):
    return send_response(
        content={'message': 'Method not allowed'},
        status_code=405
    )
