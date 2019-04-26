
__author__ = 'ACV'
import logging
from functools import wraps
from datetime import datetime
from settings import ENCODING
logger = logging.getLogger('decorators')


def logged(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        logger.debug(f'{ func.__name__ } : { request }')
        return func(request, *args, **kwargs)

    return wrapper


def log(func):
    """
    Логируем какая функция вызывается.
    """

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