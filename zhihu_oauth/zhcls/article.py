from .base import Base
from .simple_info import simple_info
from .other_obj import other_obj
from .streaming import streaming
from .generator import generator_of

from ..oauth2.setting import (
    ARTICLE_DETAIL_URL,
    ARTICLE_COMMENTS_URL,
)

__all__ = ['Article']


class Article(Base):
    def __init__(self, id, cache, session):
        super(Article, self).__init__(id, cache, session)

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
