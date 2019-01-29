from utils import send_response


def method_not_allowed(e):
    return send_response(
        content={'message': 'Method not allowed'},
        status_code=405
    )


def not_found(e):
    return send_response(
        content={'message': 'Not found'},
        status_code=404
    )
