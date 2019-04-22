from  server.protocol import make_response, validate_request
from datetime import datetime


def test_validate_positive_request():
    action_name = 'echo'
    data = 'Some data'
    request = {
        'action': action_name,
        'time': datetime.now().timestamp(),
        'data': data
    }

    assert validate_request(request) is True


def test_validate_negative_request():
    action_name = 'echo'
    data = 'Some data'

    request = {
        'action': action_name,
        'time': None,
        'data': data
    }

    assert validate_request(request) is False


def test_make_response():
    action_name = 'echo'
    user = 'Some User'
    data = 'Some data'
    code = 400

    request = {
        'action': action_name,
        'user': user,
        'time': datetime.now().timestamp(),
        }

    assert make_response(request, code, data).get('code') == code

