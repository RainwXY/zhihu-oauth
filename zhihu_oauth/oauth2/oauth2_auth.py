# coding=utf-8

from __future__ import unicode_literals

from .android_auth import ImZhihuAndroidClient
from .token import ZhihuToken

__all__ = ['ZhihuOAuth2']


class ZhihuOAuth2(ImZhihuAndroidClient):
    def __init__(self, token, api_version=None, app_version=None,
                 app_build=None, app_za=None):
        assert isinstance(token, ZhihuToken)
        super(ZhihuOAuth2, self).__init__(
            api_version, app_version, app_build, app_za)
        self._token = token

    def __call__(self, r):
        r = super(ZhihuOAuth2, self).__call__(r)
        r.headers['Authorization'] = '{type} {token}'.format(
            type=self._token.type, token=self._token.token)
        return r
