# coding=utf-8

from __future__ import unicode_literals

import functools

__all__ = ['StreamingJSON', 'streaming']


class StreamingJSON:
    def __init__(self, json_data):
        if not isinstance(json_data, (dict, list)):
            raise ValueError('Need dict or list to build StreamingJSON object.')
        self._json = json_data

    def __getattr__(self, item):
        if isinstance(self._json, dict):

            # 防止和 Python 内置关键字冲突
            if item.endswith('_'):
                item = item[:-1]
            if item in self._json:
                obj = self._json[item]
                if isinstance(obj, (dict, list)):
                    return StreamingJSON(obj)
                else:
                    return obj
            else:
                raise AttributeError("No attr {0} in my data {1}!".format(
                    item, self._json))
        else:
            raise ValueError("Can't use XX.xxx in list-like obj {0}, "
                             "please use XX[num].".format(self._json))

    def __getitem__(self, item):
        if isinstance(self._json, list) and isinstance(item, int):
            obj = self._json[item]
            if isinstance(obj, (dict, list)):
                return StreamingJSON(obj)
            else:
                return obj

        raise ValueError("Can't use XX[num] in dict-like obj {0}, "
                         "please use XX.xxx.".format(self._json))

    def __iter__(self):
        def _iter():
            for x in self._json:
                if isinstance(x, (dict, list)):
                    yield StreamingJSON(x)
                else:
                    yield x

        return _iter()

    def __len__(self):
        return len(self._json)

    def __str__(self):
        return str(self._json)

    def __repr__(self):
        return repr(self._json)


def streaming(name_in_cache=None, use_cache=True):
    def wrappers_wrapper(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            name = name_in_cache if name_in_cache else func.__name__
            if use_cache and self._cache and name in self._cache:
                cache = self._cache[name]
            else:
                self._get_data()
                if self._data and name in self._data:
                    cache = self._data[name]
                else:
                    return func(self, *args, **kwargs)
            return StreamingJSON(cache)

        return wrapper

    return wrappers_wrapper
