# coding=utf-8

from __future__ import print_function, unicode_literals

import base64
import getpass
import os

import requests

from .oauth2.login_auth import LoginAuth
from .oauth2.oauth2_auth import ZhihuOAuth2
from .oauth2.token import ZhihuToken
from .oauth2.util import login_signature
from .setting import CAPTCHA_FILE
from .utils import need_login, int_id
from .oauth2.setting import (
    CAPTCHA_URL, LOGIN_URL, LOGIN_DATA, CLIENT_ID, APP_SECRET
)
from .exception import (
    UnexpectedResponseException, NeedCaptchaException, MyJSONDecodeError
)

__all__ = ['ZhihuClient']

try:
    # noinspection PyShadowingBuiltins,PyUnresolvedReferences
    input = raw_input
except NameError:
    pass


# noinspection PyShadowingBuiltins
class ZhihuClient:
    #  client_id and secret shouldn't have default value after zhihu open api
    def __init__(self, client_id=CLIENT_ID, secret=APP_SECRET):
        self._session = requests.session()
        self._client_id = client_id
        self._secret = secret
        self._login_auth = LoginAuth(self._client_id)
        self._token = None

    def need_captcha(self):
        res = self._session.get(CAPTCHA_URL, auth=self._login_auth)
        try:
            j = res.json()
            return j['show_captcha']
        except (MyJSONDecodeError, AttributeError):
            raise UnexpectedResponseException(
                CAPTCHA_URL, res,
                'a json data with show_captcha item'
            )

    def get_captcha(self):
        self.need_captcha()
        res = self._session.put(CAPTCHA_URL, auth=self._login_auth)
        try:
            j = res.json()
            # noinspection PyDeprecation
            return base64.decodestring(j['img_base64'].encode('utf-8'))
        except MyJSONDecodeError:
            raise UnexpectedResponseException(
                CAPTCHA_URL,
                res,
                'a json string contain a img_base64 item.'
            )

    def login(self, email, password, captcha=None):
        """登录知乎的主要方法

        :param str email: 邮箱
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
                    return False, json_dict['error']['message']
            except MyJSONDecodeError:
                return False, 'UnexpectedResponse'

        data = dict(LOGIN_DATA)
        data['username'] = email
        data['password'] = password
        data['client_id'] = self._client_id

        login_signature(data, self._secret)
        res = self._session.post(LOGIN_URL, auth=self._login_auth, data=data)
        try:
            json_dict = res.json()
            if 'error' in json_dict:
                return False, json_dict['error']['message']
            else:
                self._token = ZhihuToken.from_dict(json_dict)
                self._session.auth = ZhihuOAuth2(self._token)
                return True, ''
        except (ValueError, MyJSONDecodeError):
            return False, 'UnexpectedResponse'

    def login_in_terminal(self, email=None, password=None):

        print('----- Zhihu OAuth Login -----')
        email = email or input('email: ')
        password = password or getpass.getpass('password: ')

        try:
            success, reason = self.login(email, password)
        except NeedCaptchaException:
            print('Need for a captcha, getting it......')
            captcha_image = self.get_captcha()
            with open('captcha.gif', 'wb') as f:
                f.write(captcha_image)
            print('Please open {0} for captcha'.format(
                os.path.abspath(CAPTCHA_FILE)))
            captcha = input('captcha: ')
            os.remove(os.path.abspath(CAPTCHA_FILE))
            success, reason = self.login(email, password, captcha)

        if success:
            print('Login success.')
        else:
            print('Login failed, reason: ', reason)

        return success, reason

    def create_token(self, filename, email=None, password=None):
        success, reason = self.login_in_terminal(email, password)
        if success:
            self.save_token(filename)
            print('Token file created success.')
        else:
            print('Token file created failed.')
        return success, reason

    def load_token(self, filename):
        self._token = ZhihuToken.from_file(filename)
        self._session.auth = ZhihuOAuth2(self._token)

    @need_login
    def save_token(self, filename):
        self._token.save(filename)

    def is_login(self):
        return self._token is not None

    @need_login
    def test_api(self, method, url, params=None, data=None):
        return self._session.request(method, url, params, data)

    # ----- get zhihu classes from ids -----

    @int_id
    @need_login
    def answer(self, id):
        from .zhcls.answer import Answer
        return Answer(id, None, self._session)

    @int_id
    @need_login
    def article(self, id):
        from .zhcls.article import Article
        return Article(id, None, self._session)

    @int_id
    @need_login
    def collection(self, id):
        from .zhcls.collection import Collection
        return Collection(id, None, self._session)

    @need_login
    def column(self, id):
        from .zhcls.column import Column
        return Column(id, None, self._session)

    @need_login
    def me(self):
        from .zhcls import Me

        return Me(self._token.user_id, None, self._session)

    @need_login
    def people(self, id):
        from .zhcls.people import People
        return People(id, None, self._session)

    @int_id
    @need_login
    def question(self, id):
        from .zhcls.question import Question
        return Question(id, None, self._session)

    @int_id
    @need_login
    def topic(self, id):
        from .zhcls.topic import Topic
        return Topic(id, None, self._session)
