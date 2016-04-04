from .base import Base
from .generator import generator_of
from .simple_info import simple_info
from .streaming import streaming
from .urls import (
    PEOPLE_DETAIL_URL,
    PEOPLE_ANSWERS_URL,
    PEOPLE_ARTICLES_URL,
    PEOPLE_COLLECTIONS_URL,
    PEOPLE_COLUMNS_URL,
    PEOPLE_FOLLOWERS_URL,
    PEOPLE_FOLLOWING_COLLECTIONS_URL,
    PEOPLE_FOLLOWING_COLUMNS_URL,
    PEOPLE_FOLLOWING_QUESTIONS_URL,
    PEOPLE_FOLLOWING_TOPICS_URL,
    PEOPLE_FOLLOWINGS_URL,
    PEOPLE_QUESTIONS_URL,
)

__all__ = ['ANONYMOUS', 'People']


class Anonymous:
    pass


ANONYMOUS = Anonymous()


class People(Base):
    def __init__(self, id, cache, session):
        super(People, self).__init__(id, cache, session)

    def _build_url(self):
        return PEOPLE_DETAIL_URL.format(self.id)

    # ---------- simple info ---------

    @property
    @simple_info()
    def answer_count(self):
        return None

    @property
    @simple_info()
    def articles_count(self):
        return None

    @property
    @simple_info()
    def avatar_url(self):
        return None

    @property
    @streaming()
    def business(self):
        return None

    @property
    @simple_info('favorited_count')
    def collected_count(self):
        return None

    @property
    @simple_info('favorite_count')
    def collection_count(self):
        return None

    @property
    @simple_info('columns_count')
    def column_count(self):
        return None

    @property
    def columns_count(self):
        return self.column_count

    @property
    @simple_info()
    def created_at(self):
        return None

    @property
    @simple_info()
    def description(self):
        return None

    @property
    @simple_info()
    def draft_count(self):
        return None

    @property
    @streaming()
    def education(self):
        return None

    @property
    @simple_info()
    def email(self):
        return None

    @property
    def favorite_count(self):
        return self.collection_count

    @property
    def favorited_count(self):
        return self.collected_count

    @property
    @simple_info()
    def follower_count(self):
        return None

    @property
    @simple_info('following_columns_count')
    def following_column_count(self):
        return None

    @property
    @simple_info()
    def following_count(self):
        return None

    @property
    @simple_info()
    def following_question_count(self):
        return None

    @property
    @simple_info()
    def following_topic_count(self):
        return None

    @property
    @simple_info()
    def friendly_score(self):
        return None

    @property
    @simple_info()
    def gender(self):
        return None

    @property
    @simple_info()
    def has_daily_recommend_permission(self):
        return None

    @property
    @simple_info()
    def headline(self):
        return None

    @property
    @simple_info()
    def is_active(self):
        return None

    @property
    @simple_info()
    def id(self):
        return self._id

    @property
    @simple_info()
    def is_baned(self):
        return None

    @property
    @simple_info()
    def is_bind_sina(self):
        return None

    @property
    @simple_info()
    def is_locked(self):
        return None

    @property
    @simple_info()
    def is_moments_user(self):
        return None

    @property
    @streaming()
    def location(self):
        return None

    @property
    @simple_info()
    def name(self):
        return None

    @property
    @simple_info()
    def question_count(self):
        return None

    @property
    @simple_info()
    def shared_count(self):
        return None

    @property
    @simple_info()
    def sina_weibo_name(self):
        return None

    @property
    @simple_info()
    def sina_weibo_url(self):
        return None

    @property
    @simple_info()
    def thanked_count(self):
        return None

    @property
    @simple_info()
    def uid(self):
        return None

    @property
    @simple_info()
    def voteup_count(self):
        return None

    # ---------- generators ---------

    # TODO: people.activities

    @property
    @generator_of(PEOPLE_ANSWERS_URL)
    def answers(self):
        return None

    @property
    @generator_of(PEOPLE_ARTICLES_URL)
    def articles(self):
        return None

    @property
    @generator_of(PEOPLE_COLLECTIONS_URL)
    def collections(self):
        return None

    @property
    @generator_of(PEOPLE_COLUMNS_URL)
    def columns(self):
        return None

    @property
    @generator_of(PEOPLE_FOLLOWERS_URL, 'people')
    def followers(self):
        return None

    @property
    @generator_of(PEOPLE_FOLLOWING_COLLECTIONS_URL, 'collection')
    def following_collections(self):
        return None

    @property
    @generator_of(PEOPLE_FOLLOWING_COLUMNS_URL, 'column')
    def following_columns(self):
        return None

    @property
    @generator_of(PEOPLE_FOLLOWING_QUESTIONS_URL, 'question')
    def following_questions(self):
        return None

    @property
    @generator_of(PEOPLE_FOLLOWING_TOPICS_URL, 'topic')
    def following_topics(self):
        return None

    @property
    @generator_of(PEOPLE_FOLLOWINGS_URL, 'people')
    def followings(self):
        return None

    @property
    @generator_of(PEOPLE_QUESTIONS_URL)
    def questions(self):
        return None
