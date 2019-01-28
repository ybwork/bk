from utils import send_response


def method_not_allowed(e):
    return send_response(
        {
            'message': 'Method not allowed'
        },
        405
    )
