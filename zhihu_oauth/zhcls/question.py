# coding=utf-8

from __future__ import unicode_literals

from .base import Base
from .generator import generator_of
from .simple_info import simple_info
from .streaming import streaming
from zhihu_oauth.zhcls.urls import (
    QUESTION_DETAIL_URL,
    QUESTION_ANSWERS_URL,
    QUESTION_COMMENTS_URL,
    QUESTION_FOLLOWERS_URL,
    QUESTION_TOPICS_URL,
)

__all__ = ['Question']


class Question(Base):
    def __init__(self, qid, cache, session):
        super(Question, self).__init__(qid, cache, session)

    def _build_url(self):
        return QUESTION_DETAIL_URL.format(self._id)

    # ----- simple info -----

    @property
    @simple_info()
    def allow_delete(self):
        return None

    @property
    @simple_info()
    def answer_count(self):
        return None

    @property
    @simple_info()
    def comment_count(self):
        return None

    @property
    @simple_info('except')
    def excerpt(self):
        """
        知乎返回的 json 里这一项叫做 except.... 也是醉了
        """
        return None

    @property
    @simple_info()
    def follower_count(self):
        return None

    @property
    @simple_info()
    def id(self):
        return self._id

    @property
    @simple_info()
    def detail(self):
        return None

    @property
    @streaming()
    def redirection(self):
        return None

    @property
    @streaming()
    def status(self):
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
    @simple_info()
    def updated_time(self):
        return None

    # ----- generators -----

    @property
    @generator_of(QUESTION_ANSWERS_URL)
    def answers(self):
        return None

    @property
    @generator_of(QUESTION_COMMENTS_URL)
    def comments(self):
        return None

    @property
    @generator_of(QUESTION_FOLLOWERS_URL, 'people')
    def followers(self):
        return None

    @property
    @generator_of(QUESTION_TOPICS_URL)
    def topics(self):
        return None
