# coding=utf-8

from __future__ import unicode_literals

import functools
import sys
import time
import importlib

from ..exception import UnexpectedResponseException, MyJSONDecodeError

__all__ = ['BaseGenerator', 'AnswerGenerator', 'ArticleGenerator',
           'CollectionGenerator', 'ColumnGenerator', 'CommentGenerator',
           'PeopleGenerator', 'QuestionGenerator', 'TopicGenerator']


MAX_WAIT_TIME = 8


class BaseGenerator(object):
    def __init__(self, url, session):
        self._url = url
        self._session = session
        self._index = 0
        self._data = []
        self._up = 0
        self._next_url = self._url
        self._need_sleep = 0.5
        self._extra_params = {}

    def _fetch_more(self):
        params = {}
        params.update(self._extra_params)
        res = self._session.get(self._next_url, params=params)
        try:
            json_dict = res.json()
            if 'error' in json_dict:

                # comment conversion hack
                if json_dict['error']['name'] == 'ERR_CONVERSATION_NOT_FOUND':
                    self._next_url = None

                # auto retry
                self._need_sleep *= 2
                if self._need_sleep > MAX_WAIT_TIME:
                    # meet max retry time, stop fetch
                    self._next_url = None
                else:
                    time.sleep(self._need_sleep)

                return

            self._need_sleep = 0.5
            self._up += len(json_dict['data'])
            self._data.extend(json_dict['data'])
            if json_dict['paging']['is_end']:
                self._next_url = None
            else:
                self._next_url = json_dict['paging']['next']
        except (MyJSONDecodeError, AttributeError):
            raise UnexpectedResponseException(
                self._next_url,
                res,
                'a json string, has data and paging'
            )

    def _build_obj(self, data):
        return None

    def __getitem__(self, item):
        if not isinstance(item, int):
            raise TypeError('Need an int as index, not {0}'.format(type(item)))
        while item >= self._up:
            if self._next_url is not None:
                self._fetch_more()
            else:
                raise IndexError('list index out of range')
        return self._build_obj(self._data[item])

    def __next__(self):
        try:
            obj = self[self._index]
        except IndexError:
            raise StopIteration
        self._index += 1
        return obj

    def order_by(self, what):
        self._extra_params['order_by'] = what
        self._index = 0
        self._up = 0
        self._next_url = self._url
        del self._data[:]
        return self


class AnswerGenerator(BaseGenerator):
    def __init__(self, url, session):
        super(AnswerGenerator, self).__init__(url, session)

    def _build_obj(self, data):
        from .answer import Answer
        return Answer(data['id'], data, self._session)


class ArticleGenerator(BaseGenerator):
    def __init__(self, url, session):
        super(ArticleGenerator, self).__init__(url, session)

    def _build_obj(self, data):
        from .article import Article
        return Article(data['id'], data, self._session)


class CollectionGenerator(BaseGenerator):
    def __init__(self, url, session):
        super(CollectionGenerator, self).__init__(url, session)

    def _build_obj(self, data):
        from .collection import Collection
        return Collection(data['id'], data, self._session)


class ColumnGenerator(BaseGenerator):
    def __init__(self, url, session):
        super(ColumnGenerator, self).__init__(url, session)

    def _build_obj(self, data):
        from .column import Column
        return Column(data['id'], data, self._session)


class CommentGenerator(BaseGenerator):
    def __init__(self, url, session):
        super(CommentGenerator, self).__init__(url, session)

    def _build_obj(self, data):
        from .comment import Comment
        return Comment(data['id'], data, self._session)


class PeopleGenerator(BaseGenerator):
    def __init__(self, url, session):
        super(PeopleGenerator, self).__init__(url, session)

    def _build_obj(self, data):
        from .people import People
        return People(data['id'], data, self._session)


class QuestionGenerator(BaseGenerator):
    def __init__(self, url, session):
        super(QuestionGenerator, self).__init__(url, session)

    def _build_obj(self, data):
        from .question import Question
        return Question(data['id'], data, self._session)


class TopicGenerator(BaseGenerator):
    def __init__(self, url, session):
        super(TopicGenerator, self).__init__(url, session)

    def _build_obj(self, data):
        from .topic import Topic
        return Topic(data['id'], data, self._session)


def generator_of(url_pattern, class_name=None, name_in_json=None):
    def wrappers_wrapper(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            cls_name = class_name or func.__name__
            name_in_j = name_in_json or func.__name__

            if cls_name.endswith('s'):
                cls_name = cls_name[:-1]
            cls_name = cls_name.capitalize()

            file_name = '.' + cls_name.lower()

            try:
                module = importlib.import_module(file_name, 'zhihu_oauth.zhcls')
                cls = getattr(module, cls_name)
            except (ImportError, AttributeError):
                return func(*args, **kwargs)

            # ---- the following code may cause a bug ---

            # TODO: figure out if there is a bug in this code

            if self._cache and name_in_j in self._cache and \
                    isinstance(self._cache[name_in_j], list):
                cache_list = self._cache[name_in_j]
                return (cls(cache['id'], cache, self._session)
                        for cache in cache_list)

            self._get_data()

            if self._data and name_in_j in self._data and \
                    isinstance(self._data[name_in_j], list):
                cache_list = self._data[name_in_j]
                return (cls(cache['id'], cache, self._session)
                        for cache in cache_list)

            # -----------------------------------------

            gen_cls_name = cls_name + 'Generator'
            try:
                gen_cls = getattr(sys.modules[__name__], gen_cls_name)
            except AttributeError:
                return func(*args, **kwargs)

            return gen_cls(url_pattern.format(self.id), self._session)

        return wrapper

    return wrappers_wrapper
