# coding=utf-8

from __future__ import unicode_literals

from ..exception import MyJSONDecodeError

__all__ = ['Base']


class Base(object):
    def __init__(self, zhihu_obj_id, cache, session):
        self._id = zhihu_obj_id
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
            except MyJSONDecodeError:
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

    @property
    def pure_data(self):
        return {
            'cache': self._cache,
            'data': self._data,
        }
