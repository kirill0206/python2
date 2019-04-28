__author__ = 'ACV'

from protocol import make_response
from decorators import logged, login_required


@logged
@login_required
def get_echo(request):
    data = request.get('data')
    return make_response(request, 200, data)
