# coding=utf-8

from __future__ import unicode_literals

from .android_auth import ImZhihuAndroidClient

__all__ = ['LoginAuth']


class LoginAuth(ImZhihuAndroidClient):
    def __init__(self, client_id, api_version=None, app_version=None,
                 app_build=None, app_za=None):
        super(LoginAuth, self).__init__(
            api_version, app_version, app_build, app_za)
        self._client_id = client_id

    def __call__(self, r):
        r = super(LoginAuth, self).__call__(r)
        r.headers['Authorization'] = 'oauth {0}'.format(self._client_id)
        return r
