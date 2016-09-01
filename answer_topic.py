# -*- coding: utf-8 -*-
import sys
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

    i = 200000
    j = 0
    while True:
        answerIDs = database.graph.data("match(u:User)-[:AUTHOR]->(a:Answer) where a.answer_topic_corresponded is null return a.answerId as answerId skip " + str(i) + " limit 100")
        for answerID in answerIDs:
            try:
                # flag = is_coresspoded(answerID)
                # if flag is 1:
                #     print("抓过了"+str(answerID))
                #     continue
                answer = client.answer(int(answerID["answerId"]))
                topics = answer.question.topics
                tx = database.graph.begin()
                k = 0
                for topic in topics:
                    cypher = "merge(a:Answer{answerId: '"+str(answerID["answerId"])+"'}) set a.xxx = 1  with a  merge(t:Topic{name:'"+topic.name+"'})  set t.topicId='"+str(topic.id)+"'  merge (a)-[:BELONGED]->(t)"
                    tx.run(cypher)
                    # database.graph.data(cypher)
                    k += 1
                    if k > 5:
                        break
                tx.commit()
                j += 1
                print("对应了"+str(j)+"answer->topic")
            except Exception, e:
                print(e)
                continue
        if i > 400000:
            break
        i += 100
    print("it is over")


def is_coresspoded(answerID):
    flag = database.graph.data("match(a:Answer{answerId: '"+str(answerID["answerId"])+"'}) where a.xxx = 1 return count(a) as num ")
    if flag[0]["num"] == 1:
        return 1
    else:
        return 2

def main():
    user_bestanswers()


if __name__ == '__main__':
    main()
