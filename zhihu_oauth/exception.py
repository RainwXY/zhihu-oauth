# coding=utf-8

from __future__ import unicode_literals

try:
    from json import JSONDecodeError as MyJSONDecodeError
except ImportError:
    MyJSONDecodeError = BaseException

__all__ = [
    'UnexpectedResponseException',
    'NeedCaptchaException',
    'NeedLoginException',
    'MyJSONDecodeError',
]


class UnexpectedResponseException(BaseException):
    def __init__(self, url, res, expect):
        self.url = url
        self.res = res
        self.expect = expect

    def __repr__(self):
        return 'Get an unexpected response when visit url ' \
               '"{self.url}", we expect "{self.expect}", ' \
               'but the response body is "{self.res.text}"'.format(self=self)


class UnimplementedException(BaseException):
    def __init__(self, what):
        self.what = what

    def __repr__(self):
        return 'Meet a unimplemented station: {self.what}'.format(self=self)


class NeedCaptchaException(BaseException):
    def __init__(self):
        pass

    def __repr__(self):
        return "Need a captcha to login, " \
               "please catch this exception and " \
               "use client.get_captcha() to get it."


class NeedLoginException(BaseException):
    def __init__(self, what):
        self.what = what

    def __repr__(self):
        return 'Need login to use the "{self.what}" method.'.format(self=self)


class IdMustBeIntException(BaseException):
    def __init__(self, func):
        self.func = func.__name__

    def __repr__(self):
        return "id argument of {self.func} must be int".format(self=self)
