from functools import reduce
from settings import INSTALLED_MODULES
from decorators import log


@log
def get_server_actions():
    return reduce(
        lambda value, item: value + getattr(item, 'actionnames', tuple()),
        reduce(
            lambda value, item: value + (getattr(item, 'actions', tuple()),),
            reduce(
                lambda value, item: value + (__import__(f'{item}.actions'),),
                INSTALLED_MODULES,
                tuple(),
            ),
            tuple(),
        ),
        tuple(),
    )


@log
def resolve(action, actions=None):
    action_mapper = {
        item.get('action'): item.get('controller')
        for item in actions or get_server_actions()
    }
    return action_mapper[action]