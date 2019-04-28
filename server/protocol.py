
__author__ = 'ACV'


from datetime import datetime


def validate_request(raw_request):
    request_time = raw_request.get('time')
    request_action = raw_request.get('action')

    if request_time and request_action:
        return True

    return False


def make_response(request, code, data=None):
    return {
        'action': request.get('action'),
        'user': request.get('user'),
        'time': datetime.now().timestamp(),
        'data': data,
        'code': code,
    }


def make_400(request):
    return make_response(request, 400, 'wrong request format')


def make_404(request):
    return make_response(request, 404, 'Action is not supported')


def make_403(request):
    return make_response(request, 403, 'Access denied')
