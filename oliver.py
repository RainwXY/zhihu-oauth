# -*- coding: utf-8 -*-
import sys
import json
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
import requests
import requests.packages.urllib3 as urllib3
from neo4jA import Database


ADAPTER_WITH_RETRY = requests.adapters.HTTPAdapter(
    max_retries=requests.adapters.Retry(
        total=10,
        status_forcelist=[400, 403, 404, 408, 500, 502]
    )
)

params = {"client_id": "d4f115c7d1a33aba2e67", "client_secret": "e5e2bf0ff98bc6642cf5dad6e0e7cd7c4cf5eb78"}
ISOTIMEFORMAT = "%Y-%m-%d %X"
database = Database()
request = requests.session()
request.verify = False
request.params =params
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Add auto retry for session
request.mount('http://', ADAPTER_WITH_RETRY)
request.mount('https://', ADAPTER_WITH_RETRY)

#oauth

def user_git():
    i = 0
    init_url = "https://api.github.com/users?since=0"


    while True:
        users = request.get(init_url)
        users_30 = users.json()
        for user in users_30:
            # print("时间"+time.strftime(ISOTIMEFORMAT, time.localtime()))
            # flag = is_not_grab(user)
            # if flag == 1:
            #     print("此用户已经抓过了,跳过吧")
            #     continue
            tx = database.graph.begin()
            user_info = request.get(user["url"]).json()
            user_info = analysis_user(user_info)
            user_cypher = "merge(u:User {id:"+str(user_info["id"])+"}) set u.login='"+user_info["login"]+"'" \
                            ", u.name="+user_info["name"]+", u.comapany ="+user_info["company"]+", u.blog="+user_info["blog"]+"" \
                            ", u.location="+user_info["location"]+", u.email="+user_info["email"]+", u.public_repos="+str(user_info["public_repos"])+"" \
                            ", u.public_gists="+str(user_info["public_gists"])+", u.followers="+str(user_info["followers"])+", u.following="+str(user_info["following"])+",u.type='"+user_info["type"]+"'"
            tx.run(user_cypher)
            tx.commit()
            print("user已抓取"+str(user_info["id"]))

            #following
            following_url = user["url"]+"/following"
            followings_info = request.get(following_url)
            followings = followings_info.json()

            #处理分页的数据
            while "next" in followings_info.links:
                followings_page_url = followings_info.links["next"]["url"]
                followings_info = request.get(followings_page_url)
                followings.extend(followings_info.json())
                # followings = dict(followings, **followings_info.json())

            for following in followings:
                following_cypher = "match(iu:User{id:"+str(user_info["id"])+"}) with iu merge(u:User{id:"+str(following["id"])+"}) on create set u.login='"+following["login"]+"' merge(iu)-[:FOLLOWING]->(u)"
                # tx.run(following_cypher)
                database.graph.data(following_cypher)
                print(str(user_info["id"])+"-FOLLOWING->"+str(following["id"])+"关系对应成功")
            # tx.commit()
            print("用户关系全部对应成功 "+str(user_info["id"]))

            #repos
            repos_url = user["repos_url"]
            repos_info = request.get(repos_url)
            repos = repos_info.json()
            while "next" in repos_info.links:
                repos_page_url = repos_info.links["next"]["url"]
                repos_info = request.get(repos_page_url)
                repos.extend(repos_info.json())
                # repos = dict(repos, **repos_info.json())

            print("开始repos对应")
            k = 1
            for repo in repos:
                #处理language为null的情况
                repo["language"] = json.dumps(repo["language"]) if repo["language"] else json.dumps("")
                repo["default_branch"] = json.dumps(repo["default_branch"])

                # contributors
                contributors_info = request.get(repo["contributors_url"])
                try:
                    contributors = contributors_info.json()
                except Exception,e:
                    continue
                while "next" in contributors_info.links:
                    contributors_page_url = contributors_info.links["next"]["url"]
                    contributors_info = request.get(contributors_page_url)
                    contributors.extend(contributors_info.json())
                contributor_num = len(contributors)
                contributors = None


                repos_cypher = "match(iu:User{id:"+str(user_info["id"])+"}) with iu merge(re:Repo{id:"+str(repo["id"])+"}) set re.name ='"+repo["name"]+"',re.contribute_count="+str(contributor_num)+",re.stargazers_count="+str(repo["stargazers_count"])+"," \
                                "re.watchers_count="+str(repo["watchers_count"])+",re.language="+repo["language"]+",re.has_issues="+str(repo["has_issues"])+",re.has_wiki="+str(repo["has_wiki"])+"" \
                                ",re.forks_count="+str(repo["forks_count"])+",re.watchers="+str(repo["watchers"])+",re.fork="+str(repo["fork"])+",re.default_branch="+repo["default_branch"]+" merge(iu)-[:AUTHOR]->(re)"
                database.graph.data(repos_cypher)
                print("分支对应了"+str(k)+"个")
                k += 1

            # stared
            star_url = user["url"]+"/starred"
            star_info = request.get(star_url)
            stars = star_info.json()
            while "next" in star_info.links:
                stars_page_url = star_info.links["next"]["url"]
                star_info = request.get(stars_page_url)
                stars.extend(star_info.json())
                # 开始star
            j = 1
            print("开始stars对应")
            for star in stars:
                star["language"] = json.dumps(star["language"]) if star["language"] else json.dumps("")
                star["default_branch"] = json.dumps(star["default_branch"])

                # contributors
                contributors_info = request.get(star["contributors_url"])
                try:
                    contributors = contributors_info.json()
                except Exception,e:
                    continue
                while "next" in contributors_info.links:
                    contributors_page_url = contributors_info.links["next"]["url"]
                    contributors_info = request.get(contributors_page_url)
                    contributors.extend(contributors_info.json())
                contributor_num = len(contributors)
                contributors = None


                repos_cypher = "match(iu:User{id:"+str(user_info["id"])+"}) with iu merge(re:Repo{id:"+str(star["id"])+"}) set re.name ='"+star["name"]+"',re.contribute_count="+str(contributor_num)+",re.stargazers_count="+str(star["stargazers_count"])+"," \
                                "re.watchers_count="+str(star["watchers_count"])+",re.language="+star["language"]+",re.has_issues="+str(star["has_issues"])+",re.has_wiki="+str(star["has_wiki"])+"" \
                                ",re.forks_count="+str(star["forks_count"])+",re.watchers="+str(star["watchers"])+",re.fork="+str(star["fork"])+",re.default_branch="+star["default_branch"]+" merge(iu)-[:STARED]->(re)"
                database.graph.data(repos_cypher)
                print("关注了"+str(j)+"个")
                j += 1


                    # contributor_cypher = "merge(u:User{login:'"+contributor["login"]+"'}) with u match(re:Repo{id:"+str(repo["id"])+"}) megre (u)-[:CONTRIBUTE]->(re)"
                    # database.graph.data(contributor_cypher)

            #orgs
            orgs_url = user["organizations_url"]
            orgs_info = request.get(orgs_url)
            try:
                orgs = orgs_info.json()
            except Exception ,e:
                continue
            while "next" in orgs_info.links:
                orgs_page_url = orgs_info.links["next"]["url"]
                orgs_info = request.get(orgs_page_url)
                orgs.extend(orgs_info.json())
            print("组织对应")
            x = 1
            for org in orgs:
                database.graph.data("merge(u:User{id:"+str(org["id"])+"}) on create set u.login = '"+org["login"]+"', u.type='Organization' with u match(au:User{id:"+str(user_info["id"])+"}) merge (au)-[:BELONGED]->(u)")
                print("组织了"+str(x)+"个")
                x += 1
            database.graph.data("merge(u:User {id:"+str(user_info["id"])+"}) set u.allgrab=true")
            i += 1
            print("此用户分支对应成功 "+str(user_info["id"]))
            print("终于抓取了"+str(i)+"个用户,累死宝宝了")
        if "next" in users.links:
            init_url = users.links["next"]["url"]
            print(init_url)
        else:
            break

    print("it is over")

def is_not_grab(user):
    flag = database.graph.data("match(u:User{id:"+str(user["id"])+"}) where u.grab=true return count(u) as num")
    if flag[0]["num"] > 0:
        return 1
    else:
        return 2

def analysis_user(user):
    # user_info = {}
    # user_info["id"] = user["id"]
    # user_info["login"] = user["login"]
    user["name"] = json.dumps(user["name"]) if user["name"] else "''"
    user["company"] = json.dumps(user["company"]) if user["company"] else "''"
    user["blog"] = json.dumps(user["blog"]) if user["blog"] else "''"
    user["location"] = json.dumps(user["location"]) if user["location"] else "''"
    user["email"] = json.dumps(user["email"]) if user["email"] else "''"

    return user



def main():
    user_git()


if __name__ == '__main__':
    main()