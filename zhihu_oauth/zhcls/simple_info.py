# coding=utf-8

from __future__ import unicode_literals, print_function

import functools

__all__ = ['simple_info']

try:
    # Py2
    # noinspection PyCompatibility,PyUnresolvedReferences,PyUnboundLocalVariable
    basestring
except NameError:
    # Py3
    # noinspection PyShadowingBuiltins
    basestring = str


def _can_get_from(name, data):
    return data and name in data and isinstance(data[name],
                                                (basestring, int, float))


def simple_info(name_in_cache=None):
    def wrappers_wrapper(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            name = name_in_cache if name_in_cache else func.__name__
            if self._data is not None:
                if _can_get_from(name, self._data):
                    return self._data[name]
                else:
                    return func(self, *args, **kwargs)
            elif self._cache and _can_get_from(name, self._cache):
                return self._cache[name]
            else:
                # id is important, when there is no data, _build_url need it,
                # so, just return the function result
                if name == 'id':
                    return func(self, *args, **kwargs)

                self._get_data()

                # noinspection PyTypeChecker
                if _can_get_from(name, self._data):
                    return self._data[name]
                else:
                    return func(self, *args, **kwargs)

        return wrapper

    return wrappers_wrapper
