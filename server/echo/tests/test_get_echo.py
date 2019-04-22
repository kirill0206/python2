from ..controllers import get_echo
from datetime import datetime

def test_get_echo():
    action_name = 'echo',
    data = 'Some data'

    request = {
        'action': action_name,
        'time': datetime.now().timestamp(),
        'data': data
    }

    expected_response = {
        'action': action_name,
        'user': None,
        'time': None,
        'data': data,
        'code': 200
    }

    response = get_echo(request)

    assert expected_response.get('data') == response.get('data')
