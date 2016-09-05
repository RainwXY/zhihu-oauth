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
database = Database()

# me = client.me()

def user_bestanswers():

    userIDs = database.graph.data("match(u:User{topicID:'19554298'}) where u.name<>'匿名用户' and u.grab is null return u.userId as userId order by id(u) desc skip 100 limit 50")
    for userId in userIDs:
        people = client.people(userId["userId"])
        try:
            for follower in people.followings:
                try:
                    # t1 = threading.Thread(target=insertNeo4j, args=(follower, people.id))
                    # print("启动新线程t1")
                    # t1.start()
                    flag = grab_or_not(follower)
                    if flag is 1:
                        print("此用户已经抓过,跳过"+str(follower.id))
                        continue
                    insertNeo4j(follower, people.id)
                    print("first关系成功####"+str(follower.id))
                except Exception, e:
                    print(e)
                    failure = database.graph.begin()
                    failure.run("create(f:UserFailure{id:'"+str(follower.id)+"'})")
                    failure.commit()
                    continue
                for thirdFollow in follower.followings:
                    try:
                        second_flag = second_grab_or_not(thirdFollow)
                        if second_flag is 1:
                            print("此用户已抓过"+str(thirdFollow.id))
                            continue
                        insertNeo4j(thirdFollow, follower.id)
                        database.graph.data("match(u:User{userId:'" + thirdFollow.id + "'}) set u.answer_end=true")
                        print("second关系成功********************"+str(thirdFollow.id))
                    except Exception, e:
                        print(e)
                        failure = database.graph.begin()
                        failure.run("create(f:UserFailure{id:'"+str(thirdFollow.id)+"'})")
                        failure.commit()
                        continue
                database.graph.data("match(u:User{userId:'" + follower.id + "'}) set u.allgrab=true")
            database.graph.data("match(u:User{userId:'"+people.id+"'}) set u.grab=true")
        except Exception, e:
            print(e.message)
            continue
    print("it is over")


# 二度
def second_grab_or_not(thirdFollow):
    flag = database.graph.data("match(u:User{userId:'" + thirdFollow.id + "'})-[:AUTHOR]->(a:Answer) return count(a) as num ")
    if flag[0]["num"] > 5:
        return 1
    else:
        return 2

# 一度
def grab_or_not(follower):
    flag = database.graph.data("match(u:User{userId:'" + follower.id + "'}) where u.allgrab=true return count(u) as num")
    if flag[0]["num"] >= 1:
        return 1
    else:
        return 2

def insertNeo4j(follower, userId):
    tx = database.graph.begin()
    author = userinfo(follower)
    cypher = "merge(u:User{userId: '"+author["author_id"]+"'}) on create set u.name='"+author["author_name"]+"',u.email='"+author["author_email"]+"',u.gender='"+author["author_gender"]+"'," \
                    "u.weibo='"+author["author_weibo"]+"', u.loation='"+author["author_location"]+"'," \
                    "u.business='"+author["author_business"]+"',u.education="+author["author_education"]+"," \
                    "u.employment="+author["author_employment"]+" with u match(au:User{userId :'"+str(userId)+"'}) merge(au)-[:FOLLOWING]->(u)"
    tx.run(cypher)
    print("用户关系对应成功"+str(userId)+"->"+str(author["author_id"]))
    tx.commit()

    # 回答相关
    follower_answers = follower.answers
    i = 0
    # 抓取10个回答
    for answer in follower_answers:
        # if answer.voteup_count == 0 and answer.comment_count == 0:
        #     print("此答案效率不高啊")
        #     continue
        # tx1 = database.graph.begin()
        myanswer = user_answer(answer)
        relationShip = "match(u:User{userId: '"+author["author_id"]+"'}) MERGE (u)-[:AUTHOR]->(a:Answer{answerId:'"+myanswer["answer_id"]+"'}) on create set a.excerpt="+myanswer["excerpt"]+"," \
                            "a.thanks_count="+myanswer["thanks_count"]+",a.voteup_count="+myanswer["voteup_count"]+"," \
                            "a.comment_count="+myanswer["comment_count"]+",a.question="+myanswer["title"]+""
        database.graph.data(relationShip)
        # tx1.run(relationShip)
        # tx1.commit()
        i += 1
        print("本次已经抓取了"+str(i)+"条回答")
    print("用户回答对应完毕"+str(author["author_id"])+"->"+"回答")


def userinfo(author):
    peopleInfo = {}
    peopleInfo["author_name"] = author.name
    peopleInfo["author_weibo"] = author.sina_weibo_url if author.sina_weibo_url else ''
    peopleInfo["author_email"] = author.email if author.email else ''
    temp_location = ''
    if author.locations:
        for location in author.locations:
            temp_location += location.name
    peopleInfo["author_location"] = temp_location
    # peopleInfo["author_gender"] = "male" if author.gender == 1 else "female" if author.gender == 2 else "未填"
    if author.gender == 1:
        peopleInfo["author_gender"] = "male"
    elif author.gender == 0:
        peopleInfo["author_gender"] = "female"
    else:
        peopleInfo["author_gender"] = "未填"

    peopleInfo["author_business"] = author.business.name if author.business else ""

    temp_education = ''
    if author.educations:
        for education in author.educations:
            if 'school' in education:
                temp_education += education.school.name
            if 'major' in education:
                temp_education += education.major.name
    peopleInfo["author_education"] = json.dumps(temp_education)

    temp_employment = ''
    if author.employments:
        for employment in author.employments:
            if 'company' in employment:
                temp_employment += employment.company.name
            if 'job' in employment:
                temp_employment += employment.job.name
    peopleInfo["author_employment"] = json.dumps(temp_employment)
    peopleInfo["author_id"] = str(author.id)
    return peopleInfo

def user_answer(answer):
    answerInfo = {}
    answerInfo["thanks_count"] = str(answer.thanks_count)
    answerInfo["voteup_count"] = str(answer.voteup_count)
    answerInfo["comment_count"] = str(answer.comment_count)
    answerInfo["excerpt"] = json.dumps(answer.excerpt)
    answerInfo["answer_id"] = str(answer.id)
    answerInfo["title"] = json.dumps(answer.question.title)
    return answerInfo


# def answr_topic(topics):
#     topicList = []
#     for  mytopic in topics:
#         topicInfo = {}
#         topicInfo["id"] = mytopic.id
#         topicInfo["name"] = mytopic.name
#         topicList.append(topicInfo)
#     return topicList


def main():
    user_bestanswers()


if __name__ == '__main__':
    main()
