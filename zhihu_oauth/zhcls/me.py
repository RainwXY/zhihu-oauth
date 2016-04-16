# coding=utf-8

from __future__ import unicode_literals

from .people import People
from .urls import (
    ANSWER_CANCEL_THANKS_URL,
    ANSWER_CANCEL_UNHELPFUL_URL,
    ANSWER_THANKS_URL,
    ANSWER_UNHELPFUL_URL,
    ANSWER_VOTERS_URL,
    ARTICLE_VOTE_URL,
    COLLECTION_CANCEL_FOLLOW_URL,
    COLLECTION_FOLLOWERS_URL,
    COLUMN_FOLLOWERS_URL,
    COLUMN_CANCEL_FOLLOW_URL,
    PEOPLE_CANCEL_FOLLOWERS_URL,
    PEOPLE_FOLLOWERS_URL,
    QUESTION_CANCEL_FOLLOWERS_URL,
    QUESTION_FOLLOWERS_URL,
    SELF_DETAIL_URL,
    TOPIC_CANCEL_FOLLOW_URL,
    TOPIC_FOLLOWERS_URL,
)
from .utils import get_result_or_error

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

    def vote(self, what, op='up'):
        """
        投票操作。也就是赞同，反对，或者清除（取消赞同和反对）。

        操作对象可以是答案和文章。

        :param what: 要点赞的对象，可以是 :any:`Answer` 或 :any:`Article` 对象。
        :param str op: 对于答案可取值 'up', 'down', 'clear'，
          分别表示赞同、反对和清除。
          对于文章，只能取 'up' 和 'clear'。默认值是 'up'。
        :return: 表示结果的二元组，第一项表示是否成功，第二项表示原因。
        :rtype: (bool, str)
        :raise: :any:`UnexpectedResponseException`
          当服务器回复和预期不符，不知道是否成功时。
        """
        from .answer import Answer
        from .article import Article
        if isinstance(what, Answer):
            if op not in {'up', 'down', 'clear'}:
                raise ValueError(
                    'Operate must be up, down or clear for Answer.')
            return self._common_vote(ANSWER_VOTERS_URL, what, op)
        elif isinstance(what, Article):
            if op not in {'up', 'clear'}:
                raise ValueError('Operate must be up or clear for Article')
            return self._common_vote(ARTICLE_VOTE_URL, what, op)
        else:
            raise TypeError(
                'Unable to voteup a {0}.'.format(what.__class__.__name__))

    def thanks(self, answer, thanks=True):
        """
        感谢或者取消感谢答案。

        ..  see-also::

            返回值和可能的异常同 :any:`vote` 方法

        :param  Answer answer: 要感谢的答案
        :param bool thanks: 如果是想取消感谢，请设置为 False
        """
        from .answer import Answer
        if not isinstance(answer, Answer):
            raise TypeError('This method only accept Answer object.')
        return self._common_click(answer, not thanks,
                                  ANSWER_THANKS_URL, ANSWER_CANCEL_THANKS_URL)

    def unhelpful(self, answer, unhelpful=True):
        """
        给答案点没有帮助，或者取消没有帮助。

        ..  see-also::

            返回值和可能的异常同 :any:`vote` 方法

        :param Answer answer: 要操作的答案
        :param bool unhelpful: 如果是想撤销没有帮助，请设置为 False
        """
        from .answer import Answer
        if not isinstance(answer, Answer):
            raise TypeError('This method only accept Answer object.')
        return self._common_click(answer, not unhelpful,
                                  ANSWER_UNHELPFUL_URL,
                                  ANSWER_CANCEL_UNHELPFUL_URL)

    def follow(self, what, follow=True):
        """
        关注或者取消关注问题/话题/用户/专栏/收藏夹。

        ..  see-also::

            返回值和可能的异常同 :any:`vote` 方法

        :param what: 操作对象
        :param follow: 要取消关注的话把这个设置成 False
        """
        from . import Question, Topic, People, Column, Collection
        if isinstance(what, Question):
            return self._common_click(what, not follow,
                                      QUESTION_FOLLOWERS_URL,
                                      QUESTION_CANCEL_FOLLOWERS_URL)
        elif isinstance(what, Topic):
            return self._common_click(what, not follow, TOPIC_FOLLOWERS_URL,
                                      TOPIC_CANCEL_FOLLOW_URL)
        elif isinstance(what, People):
            what._get_data()
            return self._common_click(what, not follow, PEOPLE_FOLLOWERS_URL,
                                      PEOPLE_CANCEL_FOLLOWERS_URL)
        elif isinstance(what, Column):
            return self._common_click(what, not follow, COLUMN_FOLLOWERS_URL,
                                      COLUMN_CANCEL_FOLLOW_URL)
        elif isinstance(what, Collection):
            return self._common_click(what, not follow,
                                      COLLECTION_FOLLOWERS_URL,
                                      COLLECTION_CANCEL_FOLLOW_URL)
        else:
            raise TypeError(
                'Unable to follow a {0}.'.format(what.__class__.__name__))

    def _common_click(self, what, cancel, click_url, cancel_url):
        if cancel:
            method = 'DELETE'
            url = cancel_url.format(what.id, self.id)
        else:
            method = 'POST'
            url = click_url.format(what.id)
        res = self._session.request(method, url)
        return get_result_or_error(url, res)

    def _common_vote(self, url, what, op):
        data = {
            'voteup_count': 0,
            'voting': {'up': 1, 'down': -1, 'clear': 0}[op],
        }
        url = url.format(what.id)
        res = self._session.post(url, data=data)
        return get_result_or_error(url, res)
