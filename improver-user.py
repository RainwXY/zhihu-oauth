# -*- coding: utf-8 -*-
import sys
import json
import time
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

    i = 100000
    j = 0
    while True:
        userIDs = database.graph.data("match(u:User) return u.userId as userId skip " + str(i) + " limit 100")
        for userID in userIDs:
            try:
                flag = is_coresspoded(userID)
                if flag == 1:
                    print("完善过了"+str(userID))
                    continue
                user = client.people(userID["userId"])
                if user.gender == 1:
                    gender = "male"
                elif user.gender == 0:
                    gender = "female"
                else:
                    gender = "未填"

                cypher = "match(u:User{userId:'"+userID["userId"]+"'}) set u.answer_count="+str(user.answer_count)+"," \
                        "u.articles_count="+str(user.articles_count)+",u.collection_count="+str(user.collection_count)+"," \
                        "u.collected_count="+str(user.collected_count)+",u.follower_count="+str(user.follower_count)+"," \
                        "u.following_count="+str(user.following_count)+",u.thanked_count="+str(user.thanked_count)+"," \
                        "u.voteup_count="+str(user.voteup_count)+",u.gender='"+gender+"',u.create_time='"+str(time.time())+"'"
                database.graph.data(cypher)
                for topic in user.following_topics:
                    cypher1 = "match(u:User{userId:'"+userID["userId"]+"'}) with u  match(t:Topic{name:"+json.dumps(topic.name)+"}) merge(u)-[:FOLLOWING]->(t)"
                    database.graph.data(cypher1)
                j += 1
                print("完善了"+str(j)+"user")
            except Exception, e:
                print(e)
                continue
        if i > 200000:
            break
        i += 100
    print("it is over")


def is_coresspoded(userID):
    flag = database.graph.data("match(u:User{userId: '"+userID["userId"]+"'}) where exists(u.create_time) return count(u) as num ")
    if flag[0]["num"] == 1:
        return 1
    else:
        return 2

def main():
    user_bestanswers()


if __name__ == '__main__':
    main()
