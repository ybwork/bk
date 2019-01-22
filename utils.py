from flask import jsonify


def send_json_response(message={}, status_code=200):
    response = jsonify(message)
    response.status_code = status_code
    return response
