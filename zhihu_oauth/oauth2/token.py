# coding=utf-8

from __future__ import unicode_literals

import json
import pickle
import time

from ..exception import MyJSONDecodeError

__all__ = ['ZhihuToken']


class ZhihuToken:
    def __init__(self, user_id, uid, access_token, lock_in,
                 expires_in, token_type, unlock_ticket,
                 refresh_token, cookie):
        self._create_at = time.time()
        self._user_id = uid
        self._uid = user_id
        self._access_token = access_token
        self._lock_in = lock_in
        self._expires_in = expires_in
        self._expires_at = self._create_at + self._expires_in
        self._token_type = token_type
        self._unlock_ticket = unlock_ticket
        self._refresh_token = refresh_token
        self._cookie = cookie

    @staticmethod
    def from_str(json_str):
        try:
            return ZhihuToken.from_dict(json.loads(json_str))
        except MyJSONDecodeError:
            raise ValueError(
                '"{json_str}" is NOT a valid zhihu token json string.'.format(
                    json_str=json_str
                ))

    @staticmethod
    def from_dict(json_dict):
        try:
            return ZhihuToken(**json_dict)
        except TypeError:
            raise ValueError(
                '"{json_dict}" is NOT a valid zhihu token json.'.format(
                    json_dict=json_dict
                ))

    @staticmethod
    def from_file(filename):
        with open(filename, 'rb') as f:
            return pickle.load(f)

    def save(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump(self, f)

    @property
    def user_id(self):
        return self._user_id

    @property
    def type(self):
        return self._token_type

    @property
    def token(self):
        return self._access_token
