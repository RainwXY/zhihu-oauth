# coding=utf-8

from __future__ import unicode_literals

try:
    from json import JSONDecodeError as MyJSONDecodeError
except ImportError:
    MyJSONDecodeError = BaseException
    """
    在 Py3 下是 json.JSONDecodeError。

    在 Py2 下是 BaseException，因为 Py2 的 json 模块没有提供解析异常。
    """

__all__ = [
    'UnexpectedResponseException',
    'NeedCaptchaException',
    'NeedLoginException',
    'IdMustBeIntException',
    'UnimplementedException',
    'MyJSONDecodeError',
]


class UnexpectedResponseException(BaseException):
    def __init__(self, url, res, expect):
        """
        服务器回复了和预期格式不符的数据

        :param str url: 当前尝试访问的网址
        :param request.Response res: 服务器的回复
        :param str expect: 一个用来说明期望服务器回复的数据格式的字符串
        """
        self.url = url
        self.res = res
        self.expect = expect

    def __repr__(self):
        return 'Get an unexpected response when visit url ' \
               '"{self.url}", we expect "{self.expect}", ' \
               'but the response body is "{self.res.text}"'.format(self=self)


class UnimplementedException(BaseException):
    def __init__(self, what):
        """
        处理当前遇到的情况的代码还未实现，只是开发的时候用于占位

        ..  note:: 一般用户不用管这个异常

        :param str what: 用来描述当前遇到的情况
        """
        self.what = what

    def __repr__(self):
        return 'Meet a unimplemented station: {self.what}'.format(self=self)


class NeedCaptchaException(BaseException):
    def __init__(self):
        """
        登录过程需要验证码
        """
        pass

    def __repr__(self):
        return "Need a captcha to login, " \
               "please catch this exception and " \
               "use client.get_captcha() to get it."


class NeedLoginException(BaseException):
    def __init__(self, what):
        """
        使用某方法需要登录而当前客户端未登录

        :param str what: 当前试图调用的方法名
        """
        self.what = what

    def __repr__(self):
        return 'Need login to use the "{self.what}" method.'.format(self=self)


class IdMustBeIntException(BaseException):
    def __init__(self, func):
        """
        获取对应的知乎类时，试图传递不是整数型的 ID

        :param function func: 当前试图调用的方法名
        """
        self.func = func.__name__

    def __repr__(self):
        return "id argument of {self.func} must be int".format(self=self)
