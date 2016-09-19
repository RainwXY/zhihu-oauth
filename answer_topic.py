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

    j = 0
    while True:
        answerIDs = database.graph.data("match(u:User)-[:AUTHOR]->(a:Answer) where a.answer_topic_corresponded is null return a.answerId as answerId  skip 600 limit 100")
        for answerID in answerIDs:
            try:
                # flag = is_coresspoded(answerID)
                # if flag is 1:
                #     print("抓过了"+str(answerID))
                #     continue
                answer = client.answer(int(answerID["answerId"]))
                topics = answer.question.topics
                content = json.dumps(answer.content)
                tx = database.graph.begin()
                for topic in topics:
                    cypher = "merge(a:Answer{answerId: '"+str(answerID["answerId"])+"'}) set a.answer_topic_corresponded = true, a.content = "+content+"  with a  merge(t:Topic{name:"+json.dumps(topic.name)+"})  merge (a)-[:BELONGED]->(t)"
                    tx.run(cypher)
                    # database.graph.data(cypher)
                tx.commit()
                j += 1
                print("对应了"+str(j)+"answer->topic")
            except Exception, e:
                print(e)
                continue
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
