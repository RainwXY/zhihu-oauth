from .base import Base
from .simple_info import simple_info
from .other_obj import other_obj
from .generator import generator_of

from ..oauth2.setting import (
    COLLECTION_DETAIL_URL,
    COLLECTION_ANSWERS_URL,
    COLLECTION_FOLLOWERS_URL,
    COLLECTION_COMMENTS_URL,
)


class Collection(Base):
    def __init__(self, id, cache, session):
        super(Collection, self).__init__(id, cache, session)

    def _build_url(self):
        return COLLECTION_DETAIL_URL.format(self.id)

    # ---- simple info -----

    @property
    @other_obj()
    def answer_count(self):
        return None

    @property
    @simple_info()
    def created_time(self):
        return None

    @property
    @other_obj('people')
    def creator(self):
        return None

    @property
    @simple_info()
    def comment_count(self):
        return None

    @property
    @simple_info()
    def description(self):
        return None

    @property
    @simple_info()
    def follower_count(self):
        return None

    @property
    @simple_info()
    def id(self):
        return None

    @property
    @simple_info()
    def is_public(self):
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
    @generator_of(COLLECTION_ANSWERS_URL)
    def answers(self):
        return None

    @property
    @generator_of(COLLECTION_COMMENTS_URL)
    def comments(self):
        return None

    @property
    @generator_of(COLLECTION_FOLLOWERS_URL, 'people')
    def followers(self):
        """
        知乎的这个 API 有问题，返回一些之后会将 is_end 设置为 True，
        导致无法获取到所有的关注者，并且此问题在知乎官方API上也存在
        """
        return None
