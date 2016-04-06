# Zhihu-OAuth

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

而且，这个库终是 py2 和 py3 通用的。但是 Py3 的优先级比 Py2 高，也就是说，我会优先保证在 Py3 下的稳定性和正确性。毕竟在我学的时候选了 Py3，所以对 2 与 3 的差异了解不是很清楚，Py2 只能尽力而为了，

由于现在使用的 CLIENT_ID 和 SECRET 的获取方法并不正当，所以暂时不要大规模宣传，Thanks。

## 使用

### 登录

第一种方式，直接调用登录方法，这种方式在知乎要求输入验证码时会引发 NeedCaptchaException，需要进行处理

```python
from zhihu_oauth import ZhihuClient
from zhihu_oauth.exception import NeedCaptchaException

client = ZhihuClient()

try:
    client.login('email', 'password')
except NeedCaptchaException:
    with open('a.gif', 'wb') as f:
        f.write(client.get_captcha())
    captcha = input('please input captcha:')
    client.login('email', 'password', captcha)
```

第二种方式，使用 login_in_terminal 方法，此方法可以无参数调用，将会在终端中提示用户输入用户名和密码。也可以将用户名和密码作为参数，此时将不会提示输入。

此方式在遇见知乎需要验证码时会自动将验证码保存并提示用户输入。

```python
from zhihu_oauth import ZhihuClient

client = ZhihuClient()

client.login_in_terminal() # or ('email', 'password')
```

第三种方式，载入 token 文件

```python
from zhihu_oauth import ZhihuClient

client = ZhihuClient()

client.load_token('filename')
```

在登录成功后，可使用

```python
client.save_token('filename')
```

来保存 token 文件以供将来使用。

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

客户端上的数据对比：

![知乎个人资料][zhihu-info-image]

### 获取关联信息

代码：

```python
# 获取最近 5 个回答
for _, answer in zip(range(5), me.answers):
    print(answer.question.title, answer.voteup_count)

print('----------')

# 获取点赞量最高的 5 个回答
for _, answer in zip(range(5), me.answers.order_by('votenum')):
    print(answer.question.title, answer.voteup_count)

print('----------')

# 获取最近提的 5 个问题
for _, question in zip(range(5), me.questions):
    print(question.title, question.answer_count)

print('----------')

# 获取最近发表的 5 个文章
for _, article in zip(range(5), me.articles):
    print(article.title, article.voteup_count)

```

输出：

```
如何想象诸如超立方体之类的四维空间物体？ 10
你的第一次心动献给了 ACGN 作品中的谁？ 3
大年初一差点把自己饿死在家里是一种怎样的体验？以及有没有什么建议来规划自己的日常生活？ 1
有哪些歌曲色气满满？ 27
作为程序员，自己在Github上的项目被很多人使用是什么体验？ 32
----------
只是为了好玩儿，如何学编程？ 593
计算机领域有哪些短小精悍的轮子?(仅用于教学) 268
小明打饭的问题？ 198
如何写个爬虫程序扒下知乎某个回答所有点赞用户名单？ 116
被盗版泛滥毁掉的行业，是如何一步一步走向消亡的？ 95
----------
用户「松阳先生」的主页出了什么问题？ 1
C++运算符重载在头文件中应该如何定义？ 1
亚马逊应用市场的应用都是正版的吗？ 0
Tkinter中event_generate创建的Event如何附加数据？ 1
用Android Studio开发对电脑配置的要求？ 7
----------
你们资道吗，知乎多了个新功能哟 7
谢谢你关注我呀！！！ 28
【软件推荐01】Seer——给Win加上空格预览功能 13
终于寒假惹！准备开始写东西啦~ 14
吐槽 + 更新说明 + 寒假专栏征求意见稿 10
```

Python 代码的可阅读性很强，我想应该不用解释吧……看代码和做阅读差不多…………

反正你能想到的功能差不多都有了吧，除了下面那些 TODO……

## TODO

- [x] 将 oauth2.setting 中的 API URL 放到其他合适的地方
- [x] 规范化，`__init__` 函数，`__all__` 变量，import 方式
- [x] CLIENT_ID 和 SECRET 可自定义，为知乎开放 API 申请做准备
- [x] 增加从 id 构建相应类的方法
- [x] 添加与 zhihu-py3 的速度对比
- [x] answer.save 和 article.save
- [ ] 文档 - 正在写…………好痛苦…………
- [ ] 打包成模块
- [ ] 规范的测试
- [ ] people.activities 用户动态
- [ ] topic.activities 话题动态
- [ ] article.voters 文章点赞者，貌似 OAuth2 没有这个 API
- [ ] collection.followers 这个 API 不稳定，没法返回所有关注者
- [ ] 获取用户消息。新关注者，新评论，关注的回答有新问题，有私信等。
- [ ] Me 类的各种操作，比如评论，点赞，私信……etc
- [ ] 保证对 Python 2 和 3 的兼容性

[zhihu-py3-github]: https://github.com/7sDream/zhihu-py3
[zhihu-info-image]: http://ww2.sinaimg.cn/mw690/88e401f0jw1f2l5my58zxj20xc1hc45z.jpg
[speed-compare]: https://github.com/7sDream/zhihu-oauth/blob/master/compare.md
