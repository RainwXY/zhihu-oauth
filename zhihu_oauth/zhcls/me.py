# coding=utf-8

from __future__ import unicode_literals

from .people import People
from .urls import SELF_DETAIL_URL

__all__ = ['Me']


class Me(People):
    def __init__(self, pid, cache, session):
        super(Me, self).__init__(pid, cache, session)

    def _build_url(self):
        return SELF_DETAIL_URL

        # TODO: 好多好多用户操作，比如点赞，评论，私信，之类的……
