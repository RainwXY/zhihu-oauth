# Zhihu-OAuth

[![author][badge-author]][my-zhihu] [![docs][badge-docs]][rtds-home] [![version][badge-version]][pypi] [![py-version][badge-py-version]][pypi] [![state][badge-state]][pypi] [![license][badge-license]][license]

## 简介

最近在尝试解析出知乎官方未开放的 OAuth2 接口，顺便提供优雅的使用方式，作为 [zhihu-py3][zhihu-py3-github] 项目的继任者。

恩，理论上来说也会比 zhihu-py3 更加稳定，原因如下：

- 知乎 API 相比前端 HTML 来说肯定更加稳定和规范
- 这次的代码更加规范
- 网络请求统一放在基类中
- 属性解析统一放在装饰器中，各知乎类只用于声明有哪些属性可供使用
- 统一翻页逻辑，再也不用一个地方一个逻辑了
- 翻页时的自动重试机制（虽然不知道有没有用吧）

这一新库与 zhihu-py3 相比速度更快。有关速度对比的详细信息请点击[这里][speed-compare]。

**这个库是 Py2 和 Py3 通用的！** 但是 Py3 的优先级比 Py2 高，也就是说，我会优先保证在 Py3 下的稳定性和正确性。毕竟在我学的时候选了 Py3，所以对 2 与 3 的差异了解不是很清楚，Py2 只能尽力而为了，

由于现在使用的 CLIENT_ID 和 SECRET 的获取方法并不正当，所以暂时不要大规模宣传，Thanks。

## 使用

### 安装

```base
pip install -U zhihu_oauth
```

如果安装遇到问题，请查看文档：[安装][rtds-install]

### 登录

请参见文档：[登录][rtds-login]

### 获取基础信息

代码：

```python
from zhihu_oauth import ZhihuClient

client = ZhihuClient()

client.load_token('token.pkl')

me = client.me()

print('name', me.name)
print('headline', me.headline)
print('description', me.description)

print('following topic count', me.following_topic_count)
print('following people count', me.following_topic_count)
print('followers count', me.follower_count)

print('voteup count', me.voteup_count)
print('get thanks count', me.thanked_count)

print('answered question', me.answer_count)
print('question asked', me.question_count)
print('collection count', me.collection_count)
print('article count', me.articles_count)
print('following column count', me.following_column_count)
```

输出：

```text
name 7sDream
headline 二次元普通居民，不入流程序员，http://0v0.link
description 关注本AI的话，会自动给你发私信的哟！
following topic count 35
following people count 101
followers count 1294
voteup count 2493
get thanks count 760
answered question 258
question asked 18
collection count 9
article count 7
following column count 11
```

更多功能请参见文档：[使用方法][rtds-usage]

## 文档

完整的文档可以在[这里][rtds-home]。

貌似 ReadTheDocs 在伟大的国家访问速度有点慢，建议自备手段。

## TODO

- [x] 将 oauth2.setting 中的 API URL 放到其他合适的地方
- [x] 规范化，`__init__` 函数，`__all__` 变量，import 方式
- [x] CLIENT_ID 和 SECRET 可自定义，为知乎开放 API 申请做准备
- [x] 增加从 id 构建相应类的方法
- [x] 添加与 zhihu-py3 的速度对比
- [x] answer.save 和 article.save
- [x] 打包成模块，发布到 PyPI
- [x] 用户文档
- [x] 内部实现文档（其实就是注释）
- [ ] 提供统一的 from_url 用于构建对象
- [ ] 规范的测试
- [ ] people.activities 用户动态
- [ ] topic.activities 话题动态
- [ ] article.voters 文章点赞者，貌似 OAuth2 没有这个 API
- [ ] collection.followers 这个 API 不稳定，没法返回所有关注者
- [ ] Me 类的各种操作，比如评论，点赞，私信……etc
- [ ] 获取用户消息。新关注者，新评论，关注的回答有新问题，有私信等。
- [ ] 保证对 Python 2 和 3 的兼容性

## LICENSE

MIT


[zhihu-py3-github]: https://github.com/7sDream/zhihu-py3
[speed-compare]: https://github.com/7sDream/zhihu-oauth/blob/master/compare.md

[rtds-home]: http://zhihu-oauth.readthedocs.org/zh_CN/latest
[rtds-install]: http://zhihu-oauth.readthedocs.org/zh_CN/latest/guide/install.html
[rtds-login]: http://zhihu-oauth.readthedocs.org/zh_CN/latest/guide/login.html
[rtds-usage]: http://zhihu-oauth.readthedocs.org/zh_CN/latest/guide/use.html

[badge-author]: https://img.shields.io/badge/Author-7sDream-blue.svg
[badge-docs]: https://readthedocs.org/projects/zhihu-oauth/badge/?version=latest
[badge-version]: https://img.shields.io/pypi/v/zhihu_oauth.svg
[badge-py-version]: https://img.shields.io/pypi/pyversions/zhihu_oauth.svg
[badge-state]: https://img.shields.io/pypi/status/zhihu_oauth.svg
[badge-license]: https://img.shields.io/pypi/l/zhihu_oauth.svg

[my-zhihu]: https://www.zhihu.com/people/7sdream
[pypi]: https://pypi.python.org/pypi/zhihu_oauth
[license]: https://github.com/7sDream/zhihu-oauth/blob/master/LICENSE
