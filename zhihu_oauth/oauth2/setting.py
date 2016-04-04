import urllib.parse

# ------- Zhihu OAuth Keys -------

CLIENT_ID = '8d5227e0aaaa4797a763ac64e0c3b8'
APP_SECRET = 'ecbefbf6b17e47ecb9035107866380'

# ------- Zhihu Client Info -------

API_VERSION = '3.0.16'
APP_VERSION = '3.2.0'
APP_BUILD = 'release'
APP_ZA = urllib.parse.urlencode({
    'OS': 'Android',
    'Release': '6.0.1',
    'Model': 'Nexus 7',
    'VersionName': '3.2.0',
    'VersionCode': '307',
    'Width': '1200',
    'Height': '1824',
    'Installer': '知乎',
})

# ------- Zhihu API URLs --------

ZHIHU_API_ROOT = 'https://api.zhihu.com'

# app_config - GET - 获取应用配置信息，一些彩蛋的资料

APP_CONFIG_URL = ZHIHU_API_ROOT + '/app_config'
APP_CONFIG_PARAMS = {
    'platform': 'android',
    'version': '3.2.0',
    'version_code': '307',
    'os_version': '6.0.1',
    'build': 'release',
}

# ip_domestic - GET - IP 是否是国内

IS_DOMESTIC_URL = ZHIHU_API_ROOT + '/ip_domestic'

# captcha - GET: 是否需要验证码， PUT: 获取验证码, POST: 提交验证码 - 验证码相关

CAPTCHA_URL = ZHIHU_API_ROOT + '/captcha'

# sign_in - POST - 用户登录

LOGIN_URL = ZHIHU_API_ROOT + '/sign_in'
LOGIN_DATA = {
    'client_id': CLIENT_ID,
    'grant_type': 'password',
    'source': 'com.zhihu.android',
    'signature': '',
    'timestamp': '',
    'username': '',
    'password': '',
}

# ----- 用户相关 -----

# self - GET - 获取自身资料

SELF_DETAIL_URL = ZHIHU_API_ROOT + '/people/self'

# people - GET - 详情

PEOPLE_DETAIL_URL = ZHIHU_API_ROOT + '/people/{0}'

# people.answers - GET - 回答

PEOPLE_ANSWERS_URL = PEOPLE_DETAIL_URL + '/answers'

# people.articles - GET - 文章

PEOPLE_ARTICLES_URL = PEOPLE_DETAIL_URL + '/articles'

# people.collections - GET - 收藏夹

PEOPLE_COLLECTIONS_URL = PEOPLE_DETAIL_URL + '/collections_v2'

# people.columns - GET - 专栏

PEOPLE_COLUMNS_URL = PEOPLE_DETAIL_URL + '/columns'

# people.followers - GET - 粉丝

PEOPLE_FOLLOWERS_URL = PEOPLE_DETAIL_URL + '/followers'

# people.following_collections - GET - 关注的收藏夹

PEOPLE_FOLLOWING_COLLECTIONS_URL = PEOPLE_DETAIL_URL + '/following_collections'

# people.following_columns - GET - 关注的专栏

PEOPLE_FOLLOWING_COLUMNS_URL = PEOPLE_DETAIL_URL + '/following_columns'

# people.following_questions - GET - 关注的问题

PEOPLE_FOLLOWING_QUESTIONS_URL = PEOPLE_DETAIL_URL + '/following_questions'

# people.following_topics - GET - 关注的话题

PEOPLE_FOLLOWING_TOPICS_URL = PEOPLE_DETAIL_URL + '/following_topics'

# people.followings - GET - 关注的人

PEOPLE_FOLLOWINGS_URL = PEOPLE_DETAIL_URL + '/followees'

# people.questions - GET - 用户提的问题

PEOPLE_QUESTIONS_URL = PEOPLE_DETAIL_URL + '/questions'

# ----- 答案相关 -----

# answer - GET - 详情

ANSWER_DETAIL_URL = ZHIHU_API_ROOT + '/answers/{0}'

# answer.collections - GET - 所在收藏夹

ANSWER_COLLECTIONS_URL = ANSWER_DETAIL_URL + '/collections'

# answer.comment - GET - 评论

ANSWER_COMMENTS_URL = ANSWER_DETAIL_URL + '/comments'

# answer.voters - GET - 点赞用户

ANSWER_VOTERS_URL = ANSWER_DETAIL_URL + '/voters'

# ----- 问题相关 -----

# question - GET - 详情

QUESTION_DETAIL_URL = ZHIHU_API_ROOT + '/questions/{0}'

# question.answers - GET - 回答

QUESTION_ANSWERS_URL = QUESTION_DETAIL_URL + '/answers'

# question.comments - GET - 评论

QUESTION_COMMENTS_URL = QUESTION_DETAIL_URL + '/comments'

# question.answers GET - 关注者

QUESTION_FOLLOWERS_URL = QUESTION_DETAIL_URL + '/followers'

# question.topics - GET - 所属话题

QUESTION_TOPICS_URL = QUESTION_DETAIL_URL + '/topics'

# ----- 话题相关 -----

# topic - GET - 详情

TOPIC_DETAIL_URL = ZHIHU_API_ROOT + '/topics/{0}'

# topic.activities - GET - 动态

TOPIC_ACTIVITIES_URL = TOPIC_DETAIL_URL + '/activities_new'

# topic.best_answers - GET - 精华回答

TOPIC_BEST_ANSWERS_URL = TOPIC_DETAIL_URL + '/best_answers'

# topic.best_answerers - GET - 最佳回答者

TOPIC_BEST_ANSWERERS_URL = TOPIC_DETAIL_URL + '/best_answerers'

# topic.children - GET - 子话题

TOPIC_CHILDREN_URL = TOPIC_DETAIL_URL + '/children'

# topic.children - GET - 父话题

TOPIC_PARENTS_URL = TOPIC_DETAIL_URL + '/parent'

# topic.unanswered_questions - GET - 未回答的问题

TOPIC_UNANSWERED_QUESTION = TOPIC_DETAIL_URL + '/unanswered_questions'

# ----- 收藏夹相关 -----

# collection - GET - 详情

COLLECTION_DETAIL_URL = ZHIHU_API_ROOT + '/collections/{0}'

# collection.answers - GET - 答案

COLLECTION_ANSWERS_URL = COLLECTION_DETAIL_URL + '/answers'

# collection.comments - GET - 评论

COLLECTION_COMMENTS_URL = COLLECTION_DETAIL_URL + '/comments'

# collection.followers - GET - 粉丝

COLLECTION_FOLLOWERS_URL = COLLECTION_DETAIL_URL + '/followers?offset=0'

# ----- 专栏相关 -----

# column - GET - 详情

COLUMN_DETAIL_URL = ZHIHU_API_ROOT + '/columns/{0}'

# column.articles - GET - 文章

COLUMN_ARTICLES_URL = COLUMN_DETAIL_URL + '/articles'

# column.followers - GET - 关注者

COLUMN_FOLLOWERS_URL = COLUMN_DETAIL_URL + '/followers'

# ----- 文章相关 -----

# article - GET - 详情

ARTICLE_DETAIL_URL = ZHIHU_API_ROOT + '/articles/{0}'

# article.vote - GET: 点赞用户, POST: 点赞 - 暂时无用

ARTICLE_VOTE_URL = ARTICLE_DETAIL_URL + '/voters'

# article.comments - GET - 评论

ARTICLE_COMMENTS_URL = ARTICLE_DETAIL_URL + '/comments'

# ----- 评论相关 -----

COMMENT_DETAIL_URL = ZHIHU_API_ROOT + '/comments/{0}'

# comment.replies - GET - 评论的回复

COMMENT_REPLIES_URL = COMMENT_DETAIL_URL + '/replies'

# comment.conversation - GET - 评论的对话

COMMENT_CONVERSION_URL = COMMENT_DETAIL_URL + '/conversation'
