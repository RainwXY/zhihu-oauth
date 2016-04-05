# coding=utf-8

from __future__ import unicode_literals, print_function

import os

from zhihu_oauth import ZhihuClient


TOKEN_FILE = 'token.pkl'


client = ZhihuClient()

if os.path.isfile(TOKEN_FILE):
    client.load_token(TOKEN_FILE)
else:
    client.login_in_terminal()
    client.save_token(TOKEN_FILE)

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
