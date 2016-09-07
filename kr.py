# -*- coding: utf-8 -*-
import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
from neo4j import Database
graph = Database().graph


x1 = 3
x2 = 3
x3 = 2
c = 5

## all related topics:
topicids = graph.data("match (:Topic {name:'编程'})-[:PARENT_OF*]->(t) return collect(id(t)) as ids")
topicids = topicids[0]['ids']
# graph.data("match (t:Topic) where t.name = '编程' return id(t)") ===> 66212
topicids.append(66212)

## all crawled users
users = graph.data('match (u:User {answer_topic_corresponded:true}) return collect(id(u)) as ids')
users = users[0]['ids']
print("总数为"+str(len(users)))

f = file("kr.txt", "a+")
f1 = file("kr-details.txt", "a+")
## answers of each user
for user in users:
    KR = 0
    answers = graph.data('match (u:User) -[:AUTHOR]-> (a:Answer) where id(u) = ' + str(user) + ' return u, a ')
    userId = answers[0]["u"]["userId"]
    if userId == 0:
        print("匿名用户，跳过")
        continue
    f1.write(userId+"\n")
    for answer in answers:
        answer = answer["a"]
        # print("match (a:Answer{answerId: '"+answer["answerId"]+"'}) -[:BELONGED]-> (t:Topic) where id(t) in " + str(topicids) + " return count(t) as num")
        num = graph.data("match (a:Answer{answerId: '"+answer["answerId"]+"'}) -[:BELONGED]-> (t:Topic) where id(t) in " + str(topicids) + " return count(t) as num")
        if num > 0:
            if len(answer["excerpt"]) <= 20:
                x4 = 1
            elif len(answer["excerpt"]) > 20 and len(answer["excerpt"]) < 50:
                x4 = 2
            elif len(answer["excerpt"]) >= 50 and len(answer["excerpt"]) < 100:
                x4 = 3
            else:
                x4 = 4

            KR += x1*answer["voteup_count"]+x2*answer["thanks_count"]+x3*answer["comment_count"]+x4+c
            f1.write("voteup_count 3*"+str(answer["voteup_count"])+" thanks_count 3*"+str(answer["thanks_count"])+" comment_count 2*"+str(answer["comment_count"])+" textlength "+str(x4) +" 常数 "+str(c)+"\n")
    print(userId+"-KR->"+str(KR))
    f.write(userId+"-KR->"+str(KR)+"\n")
    f.flush()
f.close()
f1.close()
