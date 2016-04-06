# coding=utf-8

from __future__ import unicode_literals

try:
    # python2
    from urllib import urlencode
except ImportError:
    # python3
    # noinspection PyUnresolvedReferences,PyCompatibility
    from urllib.parse import urlencode

ZHIHU_API_ROOT = 'https://api.zhihu.com'

# ------- Zhihu OAuth Keys -------

CLIENT_ID = '8d5227e0aaaa4797a763ac64e0c3b8'
APP_SECRET = 'ecbefbf6b17e47ecb9035107866380'

# ------- Zhihu Client Info -------

API_VERSION = '3.0.16'
APP_VERSION = '3.2.0'
APP_BUILD = 'release'
APP_ZA = urlencode({
    'OS': 'Android',
    'Release': '6.0.1',
    'Model': 'Nexus 7',
    'VersionName': '3.2.0',
    'VersionCode': '307',
    'Width': '1200',
    'Height': '1824',
    'Installer': '知乎'.encode('utf-8'),
})

# app_config - GET - 获取应用配置信息，一些彩蛋的资料

APP_CONFIG_URL = ZHIHU_API_ROOT + '/app_config'
APP_CONFIG_PARAMS = {
    'platform': 'android',
    'version': '3.2.0',
    'version_code': '307',
    'os_version': '6.0.1',
    'build': 'release',
}

# ip_domestic - GET - IP 是否是国内

IS_DOMESTIC_URL = ZHIHU_API_ROOT + '/ip_domestic'

# captcha - GET: 是否需要验证码， PUT: 获取验证码, POST: 提交验证码 - 验证码相关

CAPTCHA_URL = ZHIHU_API_ROOT + '/captcha'

# sign_in - POST - 用户登录

LOGIN_URL = ZHIHU_API_ROOT + '/sign_in'

LOGIN_DATA = {
    'grant_type': 'password',
    'source': 'com.zhihu.android',
    'client_id': '',
    'signature': '',
    'timestamp': '',
    'username': '',
    'password': '',
}
