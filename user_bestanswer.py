# -*- coding: utf-8 -*-
from zhihu_oauth import ZhihuClient
from neo4j import Database


database = Database()
tx = database.graph.begin()
client = ZhihuClient()

client.load_token('token.pkl')

# me = client.me()
# people = client.people("excited-vczh")
topic = client.topic(19554298)
answers = topic.best_answers
i = 0
for answer in answers:
    # 作者信息
    author = answer.author
    author_name = author.name
    author_weibo = author.sina_weibo_url
    temp_location = ''
    for location in author.locations:
                temp_location += location.name
    author_location = temp_location
    author_headline = author.headline
    author_gender = "male" if author.gender ==1 else "female" if author.gender ==2 else "未填"
    author_business = author.business.name if author.business else ""

    temp_education = ''
    for education in author.educations:
                if 'school' in education:
                    temp_education += education.school.name
                if 'major' in education:
                    temp_education += education.major.name
    author_education = temp_education

    temp_employment = ''
    for employment in author.employments:
                if 'company' in employment:
                    temp_employment += employment.company.name
                if 'job' in employment:
                    temp_employment += employment.job.name
    author_employment = temp_employment

    # 答案信息

    cypher = "create(u:User{name: '"+author_name+"',gender: '"+author_gender+"', " \
            "weibo: '"+author_weibo+"', loation: '"+author_location+"',headline: '"+\
             author_headline+"',business: '"+author_business+"',education: '"+\
             author_education+"',employment: '"+author_employment+"'})-[:AUTHOR]->(" \
            "b:Best_Answer{excerpt: '"+answer.excerpt+"',thanks_count: "+str(answer.thanks_count)+"," \
            "voteup_count: "+str(answer.voteup_count)+",comment_count: "+str(answer.comment_count)+",question: '"+answer.question.title+"'})"
    tx.run(cypher)
    i += 1
    if i == 20:
        tx.commit()
        tx = database.graph.begin()
# print(topic.follower_count)
# follows = topic.followers
# i = 0
# for follow in follows:
#     print(i)
#     i += 1
#
# print("总数"+str(i))
# print(topic.followers)
# print(people.answer_count)
# print(people.articles_count)
# print(people.avatar_url)
# print(people.collection_count)
# print(people.locations)
# print(people.description)
# print(people.email)