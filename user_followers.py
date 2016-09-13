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
    userIDs = ['13ba78a859eaf6b9a5b27c5c56ee8419', 'a7c7015c4ca7c3104daab2e9abfedb57', '64fa851552b5600b7c8be72165edfdaa', 'aedee3338cf0437b9f28f20c8d6dc2d1', 'cc238666dd4406d7abda8090a04503b5', '2307d4205a82926f3617da53423a049f', '0a60bd319fac005341466c38de50afc8', '4cb6d3b7b099b64c1b506c667e7306a8', '6b630094ec4c56d07eba3224e370fecc', 'ba4db02667f457a477aec36121933b97', '317fffe6dcd8df5e5b9c2d9087a4382d', '22d1cc2d518948d2f689c847258a7881', 'fd7c571a0ada1a72e42e8d7992c4a780', '3049d74682543a3f8f73b57964bf5db3', '6bfad8199c976be84f00a7bdc078d4f5', '8a6a82ca0532b6af42131f49706fc0f7', 'da4acc1b0a6197e72ca6055a67fa9d7d', '0e512d1ab8402ae4a2517b241bccec8f', 'd5ef4d4aaa08aaa331dabd8d4f79d0e9', '044eb2b3d3f9af5d1a79830d351c1dc5', '2889bfb08d752d394089da3d8b8d2b59', 'd59999d973a2e7b49a246d5754c8270a', '13d36f4d156f77e009c117b6021703e7', 'ebbe6e14adde32eba8d014b0fcc47dbd', 'c6adcb1f69bff45a74f57f4e2150dc3c', '4952252c6cee7ec5fb6e145456487621', '3212f9044005e9306aab1b61e74e7ae6', '0c6e41c0da1b18aba0b97975c1e4b09f', '2c5ce9612b1f25a3f3bf251a09c904b5', 'ced30ef2e460b4febfd77ef3038167ce', 'c477767e63254f832747e1e99329470c', 'a79cce38125d71baaf2188da72822b11', 'a6fecae6ca1389079dbb63d0b4368eba', '9959e364fc3b62367c587c4697d8a8fd', '9558cac1a967147f0318fe6b7b1a0f7b', '012fa0165014b9e7546ca9526461a7a9', '6fe49daa35fc3eb8f10d00d59cb1c45b', '40b164683dbaf1ae328756ad8bff0e82', '8bed628a9d3e752070294349bd5f0b12', '225cbdbbfac26810c6b71ce96f55de2f', 'b5a0612700ff2573650494c01895d20c', '6e1a145fbea96fe6c16eacba4cbb3d85', 'd471405572fd829578df0319618132ad', '73dea43918ac6edf7b152eea6eb87cd4', 'a482f5dabff2e9aa22e857e5bd951d17', 'fd5d50994743daf583cac4d510b20558', '33b61032ede4c22848160527ff9a9de9', 'a88640fa29ac407fd45cd45967b42a4e', '0970f947b898ecc0ec035f9126dd4e08', 'e62f00265931ac106064ccb77e876b1b']
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
