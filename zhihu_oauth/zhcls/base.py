import json


__all__ = ['Base']


class Base:

    def __init__(self, id, cache, session):
        self._id = id
        self._cache = cache
        self._session = session
        self._data = None

    def _get_data(self):
        if self._data is None:
            res = self._session.request(
                self._method(),
                url=self._build_url(),
                params=self._build_params(),
                data=self._build_data()
            )
            try:
                self._data = res.json()
            except json.JSONDecodeError:
                self._data = None

    def _build_url(self):
        return ''

    def _build_params(self):
        return None

    def _build_data(self):
        return None

    def _method(self):
        return 'GET'

    def refresh(self):
        self._data = self._cache = None

    def pure_data(self):
        return {
            'cache': self._cache,
            'data': self._data,
        }
