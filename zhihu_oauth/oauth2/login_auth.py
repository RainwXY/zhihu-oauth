from .android_auth import ImZhihuAndroidClient
from .setting import CLIENT_ID

__all__ = ['LoginAuth']


class LoginAuth(ImZhihuAndroidClient):
    def __init__(self, client_id=CLIENT_ID):
        super(LoginAuth, self).__init__()
        self.client_id = client_id

    def __call__(self, r):
        r = super(LoginAuth, self).__call__(r)
        r.headers['Authorization'] = 'oauth {0}'.format(self.client_id)
        return r
