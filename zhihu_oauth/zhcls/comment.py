# coding=utf-8

from __future__ import unicode_literals

from .base import Base
from .generator import generator_of
from .simple_info import simple_info
from zhihu_oauth.zhcls.urls import (
    COMMENT_CONVERSION_URL,
    COMMENT_REPLIES_URL,
)

__all__ = ['Comment']


class Comment(Base):
    def __init__(self, cid, cache, session):
        super(Comment, self).__init__(cid, cache, session)

    def _get_data(self):
        self._data = None

    def _build_url(self):
        return ''

    # ----- simple info -----

    @property
    @simple_info()
    def ancestor(self):
        return None

    @property
    @simple_info()
    def allow_delete(self):
        return None

    @property
    @simple_info()
    def allow_like(self):
        return None

    @property
    @simple_info()
    def allow_reply(self):
        return None

    @property
    def author(self):
        from .people import People
        if self._cache and 'author' in self._cache:
            cache = self._cache['author']
        else:
            self._get_data()
            if self._data and 'author' in self._data:
                cache = self._data['author']
            else:
                cache = None
        if cache:
            if 'member' in cache:
                cache = cache['member']
            return People(cache['id'], cache, self._session)
        else:
            return None

    @property
    @simple_info()
    def content(self):
        return None

    @property
    @simple_info()
    def created_time(self):
        return None

    @property
    @simple_info()
    def id(self):
        return None

    @property
    @simple_info()
    def is_author(self):
        return None

    @property
    @simple_info()
    def is_delete(self):
        return None

    @property
    @simple_info()
    def is_parent_author(self):
        return None

    @property
    @simple_info()
    def resource_type(self):
        return None

    @property
    @simple_info()
    def vote_count(self):
        return None

    @property
    @simple_info()
    def voting(self):
        return None

    # ----- generators -----

    @property
    @generator_of(COMMENT_REPLIES_URL, 'comment')
    def replies(self):
        return None

    @property
    @generator_of(COMMENT_CONVERSION_URL, 'comment')
    def conversation(self):
        return None
