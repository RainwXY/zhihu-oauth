from requests.auth import AuthBase

from .setting import API_VERSION, APP_VERSION, APP_BUILD, APP_ZA


__all__ = ['ImZhihuAndroidClient']


class ImZhihuAndroidClient(AuthBase):
    def __init__(self, api_version=API_VERSION, app_version=APP_VERSION,
                 app_build=APP_BUILD, app_za=APP_ZA):
        self._api_version = api_version
        self._app_version = app_version
        self._app_build = app_build
        self._app_za = app_za

    def __call__(self, r):
        r.headers['x-api-version'] = self._api_version
        r.headers['x-app-version'] = self._app_version
        r.headers['x-app-build'] = self._app_build
        r.headers['x-app-za'] = self._app_za
        return r
