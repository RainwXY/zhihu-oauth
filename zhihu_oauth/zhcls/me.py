# coding=utf-8

from __future__ import unicode_literals

from .people import People
from .urls import SELF_DETAIL_URL

__all__ = ['Me']


class Me(People):
    def __init__(self, pid, cache, session):
        """
        ..  role:: red
        ..  raw:: html

            <style> .red {color:red} </style>

        是 :class：`People` 的子类，表示当前登录的用户。
        设想中准备将用户操作（点赞，评论，收藏，私信等）放在这个类
        里实现，:red:`但是现在还没写！`

        ..  inheritance-diagram:: Me

        ..  seealso:: :class:`People`

        """
        super(Me, self).__init__(pid, cache, session)

    def _build_url(self):
        return SELF_DETAIL_URL

        # TODO: 好多好多用户操作，比如点赞，评论，私信，之类的……
