# coding=utf-8

from __future__ import unicode_literals

from .base import Base
from .generator import generator_of
from .other_obj import other_obj
from .simple_info import simple_info
from .urls import (
    COLUMN_DETAIL_URL,
    COLUMN_ARTICLES_URL,
    COLUMN_FOLLOWERS_URL,
)

__all__ = ['Column']


class Column(Base):
    def __init__(self, cid, cache, session):
        super(Column, self).__init__(cid, cache, session)

    def _build_url(self):
        return COLUMN_DETAIL_URL.format(self.id)

    # ---- simple info -----

    @property
    @simple_info('articles_count')
    def article_count(self):
        return None

    @property
    def articles_count(self):
        return self.article_count

    @property
    @other_obj('people')
    def author(self):
        return None

    @property
    @simple_info()
    def comment_permission(self):
        return None

    @property
    @simple_info()
    def description(self):
        return None

    @property
    @simple_info('followers')
    def follower_count(self):
        return None

    @property
    @simple_info()
    def id(self):
        return self._id

    @property
    @simple_info()
    def image_url(self):
        return None

    @property
    @simple_info()
    def title(self):
        return None

    @property
    @simple_info('updated')
    def updated_time(self):
        return None

    @property
    def updated(self):
        return self.updated_time

    # ----- generators -----

    @property
    @generator_of(COLUMN_ARTICLES_URL)
    def articles(self):
        return None

    @property
    @generator_of(COLUMN_FOLLOWERS_URL, 'people')
    def followers(self):
        return None
