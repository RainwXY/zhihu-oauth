# coding=utf-8

from __future__ import unicode_literals

import os

from .base import Base
from .generator import generator_of
from .other_obj import other_obj
from .simple_info import simple_info
from .streaming import streaming
from .utils import remove_invalid_char, add_serial_number, SimpleHtmlFormatter
from .urls import (
    ARTICLE_DETAIL_URL,
    ARTICLE_COMMENTS_URL,
)

__all__ = ['Article']


class Article(Base):
    def __init__(self, aid, cache, session):
        super(Article, self).__init__(aid, cache, session)

    def _build_url(self):
        return ARTICLE_DETAIL_URL.format(self.id)

    # ----- simple info -----

    @property
    @other_obj('people')
    def author(self):
        return None

    @property
    @streaming()
    def can_comment(self):
        return None

    @property
    @other_obj()
    def column(self):
        return None

    @property
    @simple_info()
    def comment_count(self):
        return None

    @property
    @simple_info()
    def comment_permission(self):
        return None

    @property
    @simple_info()
    def content(self):
        return None

    @property
    @simple_info()
    def excerpt(self):
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
    @streaming()
    def suggest_edit(self):
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
    @simple_info()
    def voteup_count(self):
        return None

    # ----- generators -----

    @property
    @generator_of(ARTICLE_COMMENTS_URL)
    def comments(self):
        return None

    # TODO: article.voters, API 接口未知

    # ----- other operate -----

    def save(self, path='.', filename=None):
        if self._cache is None:
            self._get_data()
        if filename is None:
            filename = remove_invalid_char(self.author.name)
        path = remove_invalid_char(path)
        if not os.path.isdir(path):
            os.makedirs(path)
        full_path = os.path.join(path, filename)
        full_path = add_serial_number(full_path, 'html')
        formatter = SimpleHtmlFormatter()
        formatter.feed(self.content)
        with open(full_path, 'wb') as f:
            f.write(formatter.prettify().encode('utf-8'))
