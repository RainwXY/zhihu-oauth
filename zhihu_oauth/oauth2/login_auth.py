# coding=utf-8

from __future__ import unicode_literals

from .android_auth import ImZhihuAndroidClient

__all__ = ['LoginAuth']


class LoginAuth(ImZhihuAndroidClient):
    def __init__(self, client_id):
        super(LoginAuth, self).__init__()
        self.client_id = client_id

    def __call__(self, r):
        r = super(LoginAuth, self).__call__(r)
        r.headers['Authorization'] = 'oauth {0}'.format(self.client_id)
        return r
