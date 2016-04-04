import hashlib
import hmac
import time

from .setting import APP_SECRET

__all__ = ['login_signature']


def login_signature(data: dict) -> dict:
    data['timestamp'] = str(int(time.time()))

    params = ''.join([
        data['grant_type'],
        data['client_id'],
        data['source'],
        data['timestamp'],
    ])

    data['signature'] = hmac.new(
        bytes(APP_SECRET, 'utf8'),
        bytes(params, 'utf8'),
        hashlib.sha1
    ).hexdigest()
