# -*- coding: utf-8 -*-
import sys
import json
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

from zhihu_oauth import ZhihuClient
from neo4j import Database

client = ZhihuClient()
client.load_token('token.pkl')


# me = client.me()

def user_bestanswers():
    database = Database()
    tx = database.graph.begin()
    topicId = 19550937
    topic = client.topic(topicId)
    answers = topic.best_answers
    i = 0
    for answer in answers:
        # 作者信息
        try:
            author = answer.author
            author_name = author.name
            author_weibo = author.sina_weibo_url if author.sina_weibo_url else ''
            author_email = author.email if author.email else ''
            temp_location = ''
            if author.locations:
                for location in author.locations:
                    temp_location += location.name
            author_location = temp_location
            author_gender = "male" if author.gender ==1 else "female" if author.gender ==2 else "未填"
            author_business = author.business.name if author.business else ""

            temp_education = ''
            if author.educations:
                for education in author.educations:
                    if 'school' in education:
                        temp_education += education.school.name
                    if 'major' in education:
                        temp_education += education.major.name
            author_education = json.dumps(temp_education)

            temp_employment = ''
            if author.employments:
                for employment in author.employments:
                    if 'company' in employment:
                        temp_employment += employment.company.name
                    if 'job' in employment:
                        temp_employment += employment.job.name
            author_employment = json.dumps(temp_employment)

            # 答案信息
            thanks_count = str(answer.thanks_count)
            voteup_count = str(answer.voteup_count)
            comment_count = str(answer.comment_count)
            excerpt = json.dumps(answer.excerpt)
            # print(answer.excerpt.replace("\\", "").replace("'", ""))

            cypher = "merge(u:User{userId: '"+str(author.id)+"'}) on create set u.name='"+author_name+"',u.email='"+author_email+"',u.gender='"+author_gender+"'," \
                    "u.weibo='"+author_weibo+"', u.loation='"+author_location+"'," \
                    "u.business='"+author_business+"',u.education="+author_education+"," \
                    "u.employment="+author_employment+",u.topicID='"+str(topicId)+"'"
            tx.run(cypher)
            relationShip = "match(u:User{userId: '"+str(author.id)+"'}) MERGE (u)-[:AUTHOR]->(a:Answer{answerId:'"+str(answer.id)+"'}) on create set a.excerpt="+excerpt+"," \
                            "a.thanks_count="+thanks_count+",a.voteup_count="+voteup_count+"," \
                            "a.comment_count="+comment_count+",a.question='"+answer.question.title+"'"
            tx.run(relationShip)
            # if i == 0:
            #     database.graph.data("CREATE CONSTRAINT ON (u:User) ASSERT u.id IS UNIQUE")
                # database.graph.data("CREATE CONSTRAINT ON (b:Answer) ASSERT b.id IS UNIQUE")
            i += 1
            if len(answers._data) % 20 == 0:
                if i % 20 == 0:
                    print("开始提交!")
                    tx.commit()
                    print("此时answers长度为"+str(len(answers._data)))
                    print("抓取了"+str(i)+"个用户")
                    tx = database.graph.begin()
            else:
                tx.commit()
                print("此时answers长度为"+str(len(answers._data)))
                print("此处answers单次返回长度不为20")
                print("抓取了"+str(i)+"个用户")
                tx = database.graph.begin()
        except Exception, e:
            print(e.message)
            failure = database.graph.begin()
            failure.run("create(f:UserFailure{id:'"+str(author.id)+"',exception:'"+str(e.message)+"'})")
            failure.commit()
            continue
    print("it is over")

def main():
    user_bestanswers()


if __name__ == '__main__':
    main()
