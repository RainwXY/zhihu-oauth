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
    ANSWER_DETAIL_URL,
    ANSWER_COLLECTIONS_URL,
    ANSWER_COMMENTS_URL,
    ANSWER_VOTERS_URL,
)

__all__ = ["Answer"]


class Answer(Base):
    def __init__(self, aid, cache, session):
        super(Answer, self).__init__(aid, cache, session)

    def _build_url(self):
        return ANSWER_DETAIL_URL.format(self.id)

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
    def created_time(self):
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
    @streaming('relationship')
    def if_i(self):
        return None

    @property
    @simple_info()
    def is_copyable(self):
        return None

    @property
    @simple_info()
    def is_mine(self):
        return None

    @property
    @other_obj()
    def question(self):
        return None

    @property
    @streaming()
    def suggest_edit(self):
        return None

    @property
    @simple_info()
    def thanks_count(self):
        return None

    @property
    @simple_info()
    def updated_time(self):
        return None

    @property
    @simple_info()
    def voteup_count(self):
        return None

    # ----- generators -----

    @property
    @generator_of(ANSWER_COLLECTIONS_URL)
    def collections(self):
        return None

    @property
    @generator_of(ANSWER_COMMENTS_URL)
    def comments(self):
        return None

    @property
    @generator_of(ANSWER_VOTERS_URL, 'people')
    def voters(self):
        return None

    # ----- other operate -----

    def save(self, path='.', filename=None, invalid_char=None):
        if self._cache is None:
            self._get_data()
        if filename is None:
            filename = remove_invalid_char(self.author.name, invalid_char)
        path = remove_invalid_char(path, invalid_char)
        if not os.path.isdir(path):
            os.makedirs(path)
        full_path = os.path.join(path, filename)
        full_path = add_serial_number(full_path, '.html')
        formatter = SimpleHtmlFormatter()
        formatter.feed(self.content)
        with open(full_path, 'wb') as f:
            f.write(formatter.prettify().encode('utf-8'))
