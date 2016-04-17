# coding=utf-8

from __future__ import unicode_literals

try:
    from json import JSONDecodeError as MyJSONDecodeError
except ImportError:
    MyJSONDecodeError = Exception
    """
    在 Py3 下是 json.JSONDecodeError。

    在 Py2 下是 BaseException，因为 Py2 的 json 模块没有提供解析异常。
    """

__all__ = [
    'UnexpectedResponseException',
    'GetDataErrorException',
    'NeedCaptchaException',
    'NeedLoginException',
    'IdMustBeIntException',
    'UnimplementedException',
    'MyJSONDecodeError',
]


class UnexpectedResponseException(Exception):
    def __init__(self, url, res, expect):
        """
        服务器回复了和预期格式不符的数据

        :param str|unicode url: 当前尝试访问的网址
        :param request.Response res: 服务器的回复
        :param str|unicode expect: 一个用来说明期望服务器回复的数据格式的字符串
        """
        self.url = url
        self.res = res
        self.expect = expect

    def __repr__(self):
        return 'Get an unexpected response when visit url ' \
               '"{self.url}", we expect "{self.expect}", ' \
               'but the response body is "{self.res.text}"'.format(self=self)

    __str__ = __repr__


class UnimplementedException(Exception):
    def __init__(self, what):
        """
        处理当前遇到的情况的代码还未实现，只是开发的时候用于占位

        ..  note:: 一般用户不用管这个异常

        :param str|unicode what: 用来描述当前遇到的情况
        """
        self.what = what

    def __repr__(self):
        return 'Meet a unimplemented station: {self.what}'.format(self=self)

    __str__ = __repr__


class GetDataErrorException(UnexpectedResponseException):
    def __init__(self, url, res, expect):
        """
        :class:`UnexpectedResponseException` 的子类，
        尝试获取服务器给出的错误信息。如果获取失败则显示父类的出错信息。

        ..  seealso:: :class:`UnexpectedResponseException`
        """
        super(GetDataErrorException, self).__init__(url, res, expect)
        try:
            self._reason = res.json()['error']['message']
        except (MyJSONDecodeError, KeyError):
            self._reason = None

    def __repr__(self):
        if self._reason:
            return 'A error happened when get data: {0}'.format(self._reason)
        else:
            base = super(GetDataErrorException, self).__repr__()
            return "Unknown error! " + base

    __str__ = __repr__


class NeedCaptchaException(Exception):
    def __init__(self):
        """
        登录过程需要验证码
        """
        pass

    def __repr__(self):
        return "Need a captcha to login, " \
               "please catch this exception and " \
               "use client.get_captcha() to get it."

    __str__ = __repr__


class NeedLoginException(Exception):
    def __init__(self, what):
        """
        使用某方法需要登录而当前客户端未登录

        :param str|unicode what: 当前试图调用的方法名
        """
        self.what = what

    def __repr__(self):
        return 'Need login to use the "{self.what}" method.'.format(self=self)

    __str__ = __repr__


class IdMustBeIntException(Exception):
    def __init__(self, func):
        """
        获取对应的知乎类时，试图传递不是整数型的 ID

        :param function func: 当前试图调用的方法名
        """
        self.func = func.__name__

    def __repr__(self):
        return "You must provide a integer id " \
               "to use function: {self.func}".format(self=self)

    __str__ = __repr__
