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

    i = 810140
    j = 0
    while True:
        answerIDs = database.graph.data("match(u:User)-[:AUTHOR]->(a:Answer) return a.answerId as answerId skip "+ str(i) +" limit 100")
        for answerID in answerIDs:
            try:
                answer = client.answer(int(answerID["answerId"]))
                topics = answer.question.topics
                tx = database.graph.begin()
                k = 0
                for topic in topics:
                    cypher = "create(a:AnswerX{answerId: '"+answerID["answerId"]+"'}) with a  merge(t:Topic{name:'"+topic.name+"'})  set t.topicId='"+str(topic.id)+"'  merge (a)-[:BELONGED]->(t)"
                    tx.run(cypher)
                    j += 1
                    print("对应了"+str(j)+"answer->topic")
                    k += 1
                    if k > 5:
                        break
                tx.commit()
            except Exception, e:
                print(e)
                continue
        if i > 1200000:
            break
        i += 100
        print("抓取了"+str(i)+"answer->topic")
    print("it is over")



def main():
    user_bestanswers()


if __name__ == '__main__':
    main()
