# coding=utf-8

from __future__ import unicode_literals

import os

from .base import Base
from .generator import generator_of
from .other import other_obj
from .normal import normal_attr
from .streaming import streaming
from .utils import remove_invalid_char, add_serial_number, SimpleHtmlFormatter
from .urls import (
    ARTICLE_DETAIL_URL,
    ARTICLE_COMMENTS_URL,
)

__all__ = ['Article']


class Article(Base):
    def __init__(self, aid, cache, session):
        super(Article, self).__init__(aid, cache, session)

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
        """
        ..  seealso:: :any:`Answer.can_comment`
        """
        return None

    @property
    @other_obj()
    def column(self):
        return None

    @property
    @normal_attr()
    def comment_count(self):
        return None

    @property
    @normal_attr()
    def comment_permission(self):
        """
        ..  seealso:: :any:`Answer.comment_permission`
        """
        return None

    @property
    @normal_attr()
    def content(self):
        return None

    @property
    @normal_attr()
    def excerpt(self):
        return None

    @property
    @normal_attr()
    def id(self):
        return self._id

    @property
    @normal_attr()
    def image_url(self):
        return None

    @property
    @streaming(use_cache=False)
    def suggest_edit(self):
        """
        ..  seealso:: :any:`Answer.suggest_edit`
        """
        return None

    @property
    @normal_attr()
    def title(self):
        return None

    @property
    @normal_attr('updated')
    def updated_time(self):
        return None

    @property
    @normal_attr()
    def voteup_count(self):
        return None

    # ----- generators -----

    @property
    @generator_of(ARTICLE_COMMENTS_URL)
    def comments(self):
        return None

    # TODO: article.voters, API 接口未知

    # ----- other operate -----

    def save(self, path='.', filename=None, invalid_char=None):
        """
        除了默认文件名是文章标题外，和 :any:`Answer.save` 完全一致。

        ..  seealso:: :any:`Answer.save`

        ..  note:: TIPS

            建议的使用方法：

            ..  code-block:: python

                for article in column.articles:
                    print(article.title)
                    article.save(column.title)

        """
        if self._cache is None:
            self._get_data()
        if filename is None:
            filename = remove_invalid_char(self.title, invalid_char)
            filename = filename or '没有标题'
        path = remove_invalid_char(path, invalid_char)
        if not os.path.isdir(path):
            os.makedirs(path)
        full_path = os.path.join(path, filename)
        full_path = add_serial_number(full_path, 'html')
        formatter = SimpleHtmlFormatter()
        formatter.feed(self.content)
        with open(full_path, 'wb') as f:
            f.write(formatter.prettify().encode('utf-8'))
