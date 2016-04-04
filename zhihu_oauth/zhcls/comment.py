from .base import Base
from .simple_info import simple_info
from .generator import generator_of

from ..oauth2.setting import (
    COMMENT_REPLIES_URL,
    COMMENT_CONVERSION_URL,
)


class Comment(Base):
    def __init__(self, id, cache, session):
        super(Comment, self).__init__(id, cache, session)

    def _get_data(self):
        self._data = None

    def _build_url(self):
        return ''

    # ----- simple info -----

    @property
    @simple_info()
    def ancestor(self):
        """ 不知道是干什么的，好像永远是 False
        """
        # TODO: 搞清楚 comment.ancestor 是干啥的
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
