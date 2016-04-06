# coding=utf-8

from __future__ import unicode_literals

from .im_android import ImZhihuAndroidClient

__all__ = ['LoginAuth']


class LoginAuth(ImZhihuAndroidClient):
    def __init__(self, client_id, api_version=None, app_version=None,
                 app_build=None, app_za=None):
        """
        ..  inheritance-diagram:: LoginAuth

        这个 Auth 在 :class:`.ImZhihuAndroidClient`
        的基础上加上了发送 client_id 的功能。

        :param str client_id: 客户端 ID

        ..  seealso::
            以下参数的文档参见 :meth:`.ImZhihuAndroidClient.__init__`

        :param str api_version:
        :param str app_version:
        :param str app_build:
        :param str app_za:
        """
        super(LoginAuth, self).__init__(
            api_version, app_version, app_build, app_za)
        self._client_id = client_id

    def __call__(self, r):
        """
        ..  note::
            requests 会自动调用这个方法

        此函数在 PreparedRequest 的 HTTP header
        里加上了 HTTP Authorization 头，值为 CLIENT_ID。

        由于是 :class:`.ImZhihuAndroidClient` 的子类，也会自动加上描述 APP 信息的头。

        ..  seealso::
            :meth:`.ImZhihuAndroidClient.__call__`
        """
        r = super(LoginAuth, self).__call__(r)
        r.headers['Authorization'] = 'oauth {0}'.format(self._client_id)
        return r
