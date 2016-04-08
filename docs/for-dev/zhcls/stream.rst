StreamingJSON - 流式JSON
========================

本类用于处理在 知乎 API 返回的 JSON
数据里，既不是基本数据类型，又不是另一个知乎对象的数据。

如 :any:`People.locations`，:any:`Question.suggest_edit` 等。

Class intro - 类的介绍
----------------------

..  autoclass:: zhihu_oauth.zhcls.streaming.StreamingJSON
    :members:
    :undoc-members:
    :special-members: __init__, __getitem__, __getattr__, __iter__

Ancillary decorator - 配套装饰器
--------------------------------

..  autofunction:: zhihu_oauth.zhcls.streaming.streaming
