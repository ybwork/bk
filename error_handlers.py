from utils import send_json_response


def method_not_allowed(e):
    return send_json_response(
        status_code=405
    )
