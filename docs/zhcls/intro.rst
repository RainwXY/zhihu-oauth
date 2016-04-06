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
