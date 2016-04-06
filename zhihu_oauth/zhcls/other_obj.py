# coding=utf-8

from __future__ import unicode_literals

import functools
import importlib

__all__ = ['other_obj']


def other_obj(class_name=None, name_in_json=None):
    def wrappers_wrapper(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            cls_name = class_name or func.__name__
            cls_name = cls_name.capitalize()
            name_in_j = name_in_json or func.__name__
            file_name = '.' + cls_name.lower()
            module = importlib.import_module(file_name, 'zhihu_oauth.zhcls')
            cls = getattr(module, cls_name)

            if self._cache and name_in_j in self._cache:
                cache = self._cache[name_in_j]
            else:
                self._get_data()
                if self._data and name_in_j in self._data:
                    cache = self._data[name_in_j]
                else:
                    return func(self, *args, **kwargs)
            return cls(cache['id'], cache, self._session)

        return wrapper

    return wrappers_wrapper
