# coding=utf-8

from __future__ import unicode_literals

import hashlib
import hmac
import time

__all__ = ['login_signature']


def login_signature(data, secret):
    data['timestamp'] = str(int(time.time()))

    params = ''.join([
        data['grant_type'],
        data['client_id'],
        data['source'],
        data['timestamp'],
    ])

    data['signature'] = hmac.new(
        secret.encode('utf-8'),
        params.encode('utf-8'),
        hashlib.sha1
    ).hexdigest()
