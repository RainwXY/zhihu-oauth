import functools

__all__ = ['StreamingJSON', 'streaming']


class StreamingJSON:
    def __init__(self, json_data):
        self._json = json_data

    def __getattr__(self, item):
        if isinstance(self._json, dict):
            if item in self._json:
                obj = self._json[item]
                if isinstance(obj, (dict, list)):
                    return StreamingJSON(obj)
                else:
                    return obj
            else:
                return None
        else:
            return None

    def __getitem__(self, item):
        if isinstance(self._json, list) and isinstance(item, int):
            if item < len(self._json):
                obj = self._json[item]
                if isinstance(obj, (dict, list)):
                    return StreamingJSON(obj)
                else:
                    return obj
            else:
                raise IndexError()
        return None

    def __iter__(self):
        return (x for x in self._json)

    def __len__(self):
        return len(self._json)

    def __str__(self):
        return str(self._json)

    def __repr__(self):
        return repr(self._json)


def streaming(name_in_cache=None):
    def wrappers_wrapper(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            name = name_in_cache if name_in_cache else func.__name__
            if self._cache and name in self._cache:
                cache = self._cache[name]
            else:
                self._get_data()
                cache = self._data[name]
            return StreamingJSON(cache)

        return wrapper

    return wrappers_wrapper
