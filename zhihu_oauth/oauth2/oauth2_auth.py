# coding=utf-8

from __future__ import unicode_literals

from requests.auth import AuthBase

from .token import ZhihuToken

__all__ = ['ZhihuOAuth2']


class ZhihuOAuth2(AuthBase):
    def __init__(self, token):
        assert isinstance(token, ZhihuToken)
        self._token = token

    def __call__(self, r):
        r.headers['Authorization'] = '{type} {token}'.format(
            type=self._token.type, token=self._token.token)
        return r
