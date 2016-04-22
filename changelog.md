# 更新历史

## 实验阶段

### WIP

- [fix] 修复了设置代理后因为关闭了 SSL 而造成的报 Warning 的问题

### 0.0.6 - 2016.04.21

- [fix] 修复了 `Collection` 类的 `answer_count` 属性无法使用的 bug
- [change] 由于发现知乎 API 无法获取除自己以外用户关注的收藏夹，将 `following_collections` 由 `People` 类 移动至 `Me` 类中

### 0.0.5 - 2016.04.18

- [add] `Topic` 类增加了 `followers` 属性，可获取话题关注者
- [add] `Me` 类增加了 `vote` 方法，可以给答案/文章/评论点赞同/[反对]/清除赞和反对。
- [add] `Me` 类增加了 `thanks` 方法，可以给答案点感谢/取消感谢
- [add] `Me` 类增加了 `unhelpful` 方法，可以给答案没有帮助/取消没有帮助
- [add] `Me` 类增加了 `follow` 方法，可以关注/取消关注问题/话题/用户/专栏/收藏夹
- [add] `Me` 类增加了 `block` 方法，可以屏蔽/取消屏蔽用户
- [add] `Me` 类增加了 `collect` 方法，可以将答案加入自己的收藏夹
- [add] `Me` 类增加了 `message` 方法，可以向别的用户发私信
- [add] `Me` 类增加了 `comment` 方法，可以向答案/文章/问题/收藏夹发送评论，并且支持回复特定评论
- [add] `Me` 类增加了 `delete` 方法，可以删除自己的答案/评论/收藏夹/文章

### 0.0.4 - 2016.04.16

- [change] 所有自定义异常修改为继承 `Exception` 类，遵循 Python 文档的要求。[REF](https://docs.python.org/2/library/exceptions.html#exceptions.Exception)
- [add] `ZhihuClient` 增加 `set_proxy` 方法，可设置代理
- [add] 增加了 `People` 类的 `activities` 属性，可以获取用户动态
- [fix] 修复 Python 2 下因为 `__init__.py` 文件中的 `__all__` 变量是 unicode 而造成的 `from xxx import *` 报错的 bug
- [change] 生成器不再尝试使用类内缓存的数据，而是一定会访问 API（改了一下实现，对用户接口没啥影响）
- [add] 小小的增加了一点没啥用的测试

### 0.0.3 - 2016.04.09

- [add] 增加了 `ZhihuClient.from_url` 方法，传入合法的知乎网址，就能生成对应的对象
- [add] 给 `BaseGenerator` 增加了 `add_params` 和 `set_params`  方法
- [fix] 修复了 `BaseGenerator` 在 Python 2 下有问题的情况。
- [fix] 修复了当用户的 `locations`，`educations`，`business`，`employments` 等属性值不存在强行获取会出错的 bug
- [add] 写完了文档
- [change] 改变了好多内部类名和变量名，不过对外部接口没有影响

### 0.0.2 - 2016.04.07

- [fix] 修复错误的 BASE_HTML_HEADER 值。原值会导致 html 文件在 Firefox 中打开时，由于没有编码信息显示而不正确的问题。
- [add] 完善文档，用户文档基本写完。

### 0.0.1 - 2016.04.07

首次发布，提供基础功能。
