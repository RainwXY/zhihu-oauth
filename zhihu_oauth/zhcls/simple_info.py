import functools


__all__ = ['simple_info']


def can_get_from(name, data):
    return data and name in data and isinstance(data[name], (str, int, float))


def simple_info(name_in_cache=None):
    def wrappers_wrapper(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            name = name_in_cache if name_in_cache else func.__name__
            if self._data is not None:
                if can_get_from(name, self._data):
                    return self._data[name]
                else:
                    return func(self, *args, **kwargs)
            elif self._cache and can_get_from(name, self._cache):
                return self._cache[name]
            else:
                self._get_data()
                if can_get_from(name, self._data):
                    return self._data[name]
                else:
                    return func(self, *args, **kwargs)
        return wrapper
    return wrappers_wrapper
