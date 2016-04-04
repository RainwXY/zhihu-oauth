from .exception import NeedLoginException

__all__ = ['NeedLoginException']


def need_login(func):
    def wrapper(self, *args, **kwargs):
        if self.is_login():
            return func(self, *args, **kwargs)
        else:
            raise NeedLoginException(func.__name__)

    return wrapper
