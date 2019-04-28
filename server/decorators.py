
__author__ = 'ACV'

import logging
from functools import wraps
from datetime import datetime
from protocol import make_403
from settings import ENCODING
import zlib


logger = logging.getLogger('decorators')


def logged(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        logger.debug(f'{ func.__name__ } : { request }')
        return func(request, *args, **kwargs)

    return wrapper


def log(func):

    def wrap_log(*args, **kwargs):
        name = func.__name__
        LOG_FILE = 'log/function.log'
        logger = logging.getLogger('function')
        logger.setLevel(logging.DEBUG)

        fh = logging.FileHandler(LOG_FILE, encoding=ENCODING)
        fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        formatter = logging.Formatter(fmt)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        logger.info(f'Функция {name} вызвана из функции {super.__name__}')

        return func

    return wrap_log


def login_required(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if request.get('user'):
            return func(request, *args, **kwargs)

        return make_403(request)

    return wrapper


def compressed(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        b_request = zlib.decompress(request)
        b_response = func(b_request, *args, **kwargs)
        return zlib.compress(b_response)

    return wrapper
