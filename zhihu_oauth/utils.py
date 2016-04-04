import functools

from .exception import NeedLoginException, IdMustBeIntException

__all__ = ['need_login', 'int_id']


def need_login(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        if self.is_login():
            return func(self, *args, **kwargs)
        else:
            raise NeedLoginException(func.__name__)

    return wrapper


def int_id(func):
    @functools.wraps(func)
    def wrapper(self, id, *args, **kwargs):
        if not isinstance(id, int):
            raise IdMustBeIntException(func)
        return func(self, id, *args, **kwargs)

    return wrapper
