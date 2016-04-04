from .base import Base
from .simple_info import simple_info
from .generator import generator_of

from ..oauth2.setting import (
    TOPIC_DETAIL_URL,
    TOPIC_BEST_ANSWERS_URL,
    TOPIC_BEST_ANSWERERS_URL,
    TOPIC_CHILDREN_URL,
    TOPIC_PARENTS_URL,
    TOPIC_UNANSWERED_QUESTION,
)


class Topic(Base):
    def __init__(self, id, cache, session):
        super(Topic, self).__init__(id, cache, session)

    def _build_url(self):
        return TOPIC_DETAIL_URL.format(self.id)

    # ---- simple info -----

    @property
    @simple_info()
    def avatar_url(self):
        return None

    @property
    @simple_info('best_answers_count')
    def best_answer_count(self):
        return None

    @property
    def best_answers_count(self):
        return self.best_answer_count

    @property
    @simple_info()
    def id(self):
        return self._id

    @property
    @simple_info()
    def introduction(self):
        return None

    @property
    @simple_info()
    def excerpt(self):
        return None

    @property
    def father_count(self):
        return self.parent_count

    @property
    @simple_info('followers_count')
    def follower_count(self):
        return None

    @property
    def followers_count(self):
        return self.follower_count

    @property
    @simple_info()
    def name(self):
        return None

    @property
    @simple_info('father_count')
    def parent_count(self):
        return None

    @property
    @simple_info('questions_count')
    def question_count(self):
        return None

    @property
    def questions_count(self):
        return self.question_count

    @property
    @simple_info()
    def unanswered_count(self):
        return None

    # ----- generators -----

    # TODO: topic.activities

    @property
    @generator_of(TOPIC_BEST_ANSWERS_URL, 'answer')
    def best_answers(self):
        return None

    @property
    @generator_of(TOPIC_BEST_ANSWERERS_URL, 'people')
    def best_answerers(self):
        return None

    @property
    @generator_of(TOPIC_CHILDREN_URL, 'topic')
    def children(self):
        return None

    @property
    @generator_of(TOPIC_PARENTS_URL, 'topic')
    def parents(self):
        return None

    @property
    @generator_of(TOPIC_UNANSWERED_QUESTION, 'question')
    def unanswered_questions(self):
        return None
