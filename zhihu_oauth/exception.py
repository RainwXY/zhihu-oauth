import requests

__all__ = [
    "UnexpectedResponseException",
    "NeedCaptchaException",
    "NeedLoginException"
]


class UnexpectedResponseException(BaseException):
    def __init__(self, url: str, res: requests.Response, expect: str):
        self.url = url
        self.res = res
        self.expect = expect

    def __str__(self):
        return 'Get an unexpected response when visit url ' \
               '"{self.url}", we expect "{self.expect}", ' \
               'but the response body is "{self.res.content}"'.format(self=self)


class UnimplementedException(BaseException):
    def __init__(self, what: str):
        self.what = what

    def __str__(self):
        return 'Meet a unimplemented station: {self.what}'.format(self=self)


class NeedCaptchaException(BaseException):
    def __init__(self):
        pass

    def __str__(self):
        return "Need a captcha to login, " \
               "please catch this exception and " \
               "use client.get_captcha() to get it."


class NeedLoginException(BaseException):
    def __init__(self, what: str):
        self.what = what

    def __str__(self):
        return 'Need login to use the "{self.what}" method.'.format(self=self)
