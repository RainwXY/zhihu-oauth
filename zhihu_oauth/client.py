import base64
import getpass
import json
import os

import requests

from .utils import need_login
from .exception import UnexpectedResponseException, NeedCaptchaException
from .oauth2 import LoginAuth
from .oauth2.oauth2_auth import ZhihuOAuth2
from .oauth2.setting import CAPTCHA_URL, LOGIN_URL, LOGIN_DATA
from .oauth2.token import ZhihuToken
from .oauth2.util import login_signature
from .setting import CAPTCHA_FILE

__all__ = ['ZhihuClient']


class ZhihuClient:
    def __init__(self):
        self._session = requests.session()
        self._login_auth = LoginAuth()
        self._token = None

    def need_captcha(self):
        res = self._session.get(CAPTCHA_URL, auth=self._login_auth)
        try:
            j = res.json()
            return j['show_captcha']
        except (json.JSONDecodeError, AttributeError):
            raise UnexpectedResponseException(
                CAPTCHA_URL, res,
                'a json data with show_captcha item'
            )

    def get_captcha(self):
        self.need_captcha()
        res = self._session.put(CAPTCHA_URL, auth=self._login_auth)
        try:
            j = res.json()
            return base64.decodebytes(bytes(j['img_base64'], 'utf8'))
        except json.JSONDecodeError:
            raise UnexpectedResponseException(
                CAPTCHA_URL,
                res,
                'a json string contain a img_base64 item.'
            )

    def login(self, username: str, password: str, captcha: str = None):
        """登录知乎的主要方法

        :param str username: 用户名，可以为手机或邮箱
        :param str password: 密码
        :param str captcha: 验证码，可以为空

        :rtype: tuple(bool, str)
        :return: 二元元组，第一个元素表示是否成功，第二个元素表示失败原因
        """

        if captcha is None:
            if self.need_captcha():
                raise NeedCaptchaException
        else:
            res = self._session.post(
                CAPTCHA_URL,
                auth=self._login_auth,
                data={'input_text': captcha}
            )
            try:
                json_dict = res.json()
                if 'error' in json_dict:
                    return False, json_dict['error']
            except json.JSONDecodeError:
                return False, 'UnexpectedResponse'

        data = dict(LOGIN_DATA)
        data['username'] = username
        data['password'] = password

        login_signature(data)
        res = self._session.post(LOGIN_URL, auth=LoginAuth(), data=data)
        try:
            json_dict = res.json()
            if 'error' in json_dict:
                return False, json_dict['error']
            else:
                self._token = ZhihuToken.from_dict(json_dict)
                self._session.auth = ZhihuOAuth2(self._token)
                return True, ''
        except (ValueError, json.JSONDecodeError):
            return False, 'UnexpectedResponse'

    def login_in_terminal(self, username=None, password=None):

        print('----- Zhihu OAuth Login -----')
        username = username or input('username: ')
        password = password or getpass.getpass('password: ')

        try:
            success, reason = self.login(username, password)
        except NeedCaptchaException:
            print('Need for a captcha, getting it......')
            captcha_image = self.get_captcha()
            with open('captcha.gif', 'wb') as f:
                f.write(captcha_image)
            print('Please open {0} for captcha'.format(
                os.path.abspath(CAPTCHA_FILE)))
            captcha = input('captcha: ')
            success, reason = self.login(username, password, captcha)

        if success:
            print('Login successful.')
        else:
            print('Login failed, reason: ', reason)

    def load_token(self, filename):
        self._token = ZhihuToken.from_file(filename)
        self._session.auth = ZhihuOAuth2(self._token)

    @need_login
    def save_token(self, filename):
        self._token.save(filename)

    def is_login(self) -> bool:
        return self._token is not None

    @need_login
    def test_api(self, method, url, params=None, data=None):
        return self._session.request(method, url, params, data)

    @need_login
    def me(self):
        from .zhcls import Me

        return Me(self._token.user_id, None, self._session)
