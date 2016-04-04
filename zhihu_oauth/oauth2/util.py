import hashlib
import hmac
import time

__all__ = ['login_signature']


def login_signature(data: dict, secret: str) -> dict:
    data['timestamp'] = str(int(time.time()))

    params = ''.join([
        data['grant_type'],
        data['client_id'],
        data['source'],
        data['timestamp'],
    ])

    data['signature'] = hmac.new(
        bytes(secret, 'utf8'),
        bytes(params, 'utf8'),
        hashlib.sha1
    ).hexdigest()
