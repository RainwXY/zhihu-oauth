Intro - 知乎类文档阅读说明
==========================

..  py:module:: zhihu_oauth.zhcls.answer.Answer
    :noindex:

..  note:: 常见属性

    如果一个属性没有说明，则表示：

    - 它的名称已经把自己描述的足够清楚了。
    - 如果它是个单数，表示直接通过 ``.`` 操作符，
      能直接获取到基本类型 ``(str, int, float, bool)`` 的数据，或另一个知乎对象。
    - 如果它是个复数，表示直接通过 ``.`` 操作符，
      能获取到一个生成器，生成它所表示的知乎对象列表。

    ..  note:: 举例

        - answer.\ :meth:`voteup_count` 表示一个答案获得的赞同数（很明显是个 ``int``）。
        - answer.\ :meth:`author` 表示答案的作者（很明显应该是 :class:`.People` 类）。
        - answer.\ :meth:`voters` 表示答案的点赞者（:class:`.People` 对象的生成器）。


..  note:: JSON 对象属性

    如果我说明了一个属性的常见返回值，则表示

    - 它返回的是一个 :class:`.StreamingJSON` 对象，可以想像成一个 JS Object。
    - 它的属性可通过 ``.`` 和 ``[]`` 操作符进行遍历。

    ..  note:: 举例

        answer.\ :meth:`suggest_edit` 的常见返回值是

        .. code-block:: python

            {
                'status': True,
                'title': '为什么回答会被建议修改',
                'tip': '作者修改内容通过后，回答会重新显示。如果一周内未得到有效修改，回答会自动折叠',
                'reason': '回答被建议修改：\\n不宜公开讨论的政治内容',
                'url': 'zhihu://questions/24752645'
            }

        表示我们可以

        - 通过 ``answer.suggest_edit.status`` 取到 ``True``
        - 通过 ``answer.suggest_edit.reason`` 取到 ``'回答被建议修改：\n不宜公开讨论的政治内容'``


..  note:: 坑爹的知乎

    这个库遵循一下原则：

    - 点赞一律用 vote，点赞者用 voter
    - 收藏夹用 collection，收藏用 collect
    - 某某某的数量一律用 ``xxx_count``，``xxx`` 使用单数形式
    - 某某某的生成器一律用 ``xxxs``，即 ``xxx`` 的复数形式

    例： :any:`Column.article_count` 专栏的文章数

    例： :any:`Column.articles` 专栏所有文章的生成器

    知乎返回的 JSON 大部分都很统一，比如用词的单复数，
    用 vote 还是 like 表示点赞，等等这些。

    但是就是有那么几个不合群。

    如果你看到某个类有两个差不多的属性，他们的差别只是

    - 某一个属性多了个 s
      （比如 :any:`Column.article_count` 和 :any:`Column.articles_count`）
    - 两个属性意思相同
      （比如 :any:`People.favorited_count` 和 :any:`People.collected_count`）

    那么：

    - 有 s 的版本是我为了兼容知乎的原始数据加上的别名。
    - 其中一个属性是我强行修改成符合我自己规范的名字。

    这种做法只是为了方便用惯了原始数据的同学们，其实两个方法
    无任何区别（当然，除了名字）。
