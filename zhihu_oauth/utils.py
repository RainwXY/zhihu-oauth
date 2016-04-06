# coding=utf-8

from __future__ import unicode_literals

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
    def wrapper(self, some_id, *args, **kwargs):
        if not isinstance(some_id, int):
            raise IdMustBeIntException(func)
        return func(self, some_id, *args, **kwargs)

    return wrapper
