# coding=utf-8

from __future__ import unicode_literals

from requests.auth import AuthBase

from .setting import API_VERSION, APP_VERSION, APP_BUILD, APP_ZA

__all__ = ['ImZhihuAndroidClient']


class ImZhihuAndroidClient(AuthBase):
    def __init__(self, api_version=None, app_version=None,
                 app_build=None, app_za=None):
        self._api_version = api_version or API_VERSION
        self._app_version = app_version or APP_VERSION
        self._app_build = app_build or APP_BUILD
        self._app_za = app_za or APP_ZA

    def __call__(self, r):
        r.headers['x-api-version'] = self._api_version
        r.headers['x-app-version'] = self._app_version
        r.headers['x-app-build'] = self._app_build
        r.headers['x-app-za'] = self._app_za
        return r
