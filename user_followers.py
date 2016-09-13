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

    # userIDs = database.graph.data("match(u:User{topicID:'19554298'}) where u.name<>'匿名用户' and u.grab is null return u.userId as userId order by id(u) asc skip 150 limit 50")
    userIDs = ['d2aa63540e4481bbab493175a262a042', '9e9ee1c749f6be0966ea5cea3a38884e', '47d3a73288d62256902ce9209acb3b35', '8aad4f38cf19a691ef2135d3a85bb612', 'e3a9ce94cda3a3f8acaf6da62f0b75b3', '557cc99bfe762006cbe8be655320af2b', '5a89e9dce88916bd01000d7f9985af94', '4c9dd7ce259e3e6ae2f0fa6ca42801ee', '07cb6860e9028ac1d987a5ab1c50c71e', '6dd067bf5573f2a38d487ab6f67b0431', 'a61ff943505b062db7cfceb36ab03014', '6ef2e77274cb0719253a577665cf690e', '7f3e9504e4fad3ff0205e33e9c1b008d', '508b28aa428e24fdabe3a89773ed3b22', 'af62ea77af08fa35799f843b60badd96', '446e9b4a22efcb71fec70800df455995', '7962727afd727f3fb7c27f7c70482881', 'c379ed1787150ed1a16124d279d1aeed', 'c3e462c36fdfa22e4eaebcb0323e39c9', 'f878db365246325edc35055891fb50f1', 'b830f90d42560328acfd2a85ffcfc35d', '4c0b95ee7a64010cd92cb88809349def', 'c8d22cca942a39ba1e554947a7361834', 'b53d00a3f1ed7e2766ba6bd5d8b8b77b', '7b6393283b8c861346793e7e61dacfd0', '86858a7a4aa77d290364625efcaacb70', '0630bd0fc3a60f77bc9b4f0edb0b5f98', 'af5220816d1bbb32f315611ef05659d6', '2fbe89f73d184baafe25c3e1bd9453ad', '126c270e54b9c78b800c0ee716dc1533', 'ff3ffafc788874278bac775977dd8bf1', '81e52da0a8189e95f7106160d7e8633e', '71f60bff956386a418c70db7fd65c0de', '0b6d6678b208a32e620775464bfdc0ec', 'c1c892f179f95da8b37a1dc604839d2c', 'f034af842cad3109523a21937a5a2fbf', '4920fca107ec266a26bf578ff112a6d3', 'fd51f37ac298387052e18e73158e3187', '7e014672f2f2cca26ac57b0e4f9fa359', 'a7e9266e7a6793e5843bd35d375a1cc5', '33b6fa3aae4eeb70fb0ce62e9bd358f7', 'b13dd95b2351a49867d3ac60c7670fe3', 'fd3dbdff0811166a87250acb815e03dd', 'eaf435b228ce0b038a4afe8203f59b49', '5ae91eb539f2dda88707cd2ebce3a4c2', '71637fe077b9a2d7be320e2800ccd818', '3d5b47d91b2d8283e9189c96e75b554e', '64611505e2b3fa65234b91b0136d4dd7', 'd2fe6ae843a10d589b8a0bebf136dda8', '68bb20e3a37968e48b34a4a8d07fef8e', 'ea31ec803eef405b08c99a1e38ba7439']
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
                            print("此二度用户已抓过"+str(thirdFollow.id))
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
    flag = database.graph.data("match(u:User{userId:'" + thirdFollow.id + "'}) where u.answer_end=true return count(u) as num ")
    if flag[0]["num"] >= 1:
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
