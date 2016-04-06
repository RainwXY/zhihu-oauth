# coding=utf-8

from __future__ import unicode_literals

CAPTCHA_FILE = 'captcha.gif'
"""
请求验证码后储存文件名的默认值，现在的值是当前目录下的 captcha.gif。

仅在 :meth:`.ZhihuClient.login_in_terminal` 中被使用。
"""
