# -*- coding: utf-8 -*-

import json
import xlsxwriter
import sys
reload(sys)
sys.setdefaultencoding('utf-8')



  # "topicID": "19554298",
  #         "education": "\"武汉大学遥感图像处理\"",
  #         "weibo": "http://weibo.cn/u/3075142565",
  #         "gender": "male",
  #         "business": "",
  #         "name": "李昭鸿",
  #         "loation": "武汉大学",
  #         "employment": "\"\"",
  #         "userId": "b56416f32d38f5d9f3916541effaff0a",
  #         "email": "",
  #         "answer_topic_corresponded": true

def main():
    workbook = xlsxwriter.Workbook('user2.xlsx')
    worksheet = workbook.add_worksheet()
    titles = ["序号", "name", "gender", "location", "education", "business", "employment", "email", "weibo"]
    row = 0
    column = 0
    for title in titles:
        worksheet.write(row, column, title)
        column += 1

    jsonFile = file("user2.json", "r")
    userInfos = json.loads(jsonFile.read())['data']
    # f = file("users.txt", "a+")
    row = 1
    for userInfo in userInfos:
        # print(user_url)
        # user = UserInfo(user_url)
        # userInfoMap = user.getUserInfo(userInfo["id"])
        # f.write(json.dumps(userInfoMap)+"\n")
        worksheet.write(row, 0, str(row - 1))
        worksheet.write(row, 1, userInfo["row"][0]["name"])
        worksheet.write(row, 2, userInfo["row"][0]["gender"])
        worksheet.write(row, 3, userInfo["row"][0]["loation"])
        worksheet.write(row, 4, userInfo["row"][0]["education"])
        worksheet.write(row, 5, userInfo["row"][0]["business"])
        worksheet.write(row, 6, userInfo["row"][0]["employment"])
        worksheet.write(row, 7, userInfo["row"][0]["email"])
        worksheet.write(row, 8, userInfo["row"][0]["weibo"])
       
        row += 1
    jsonFile.close()
    # f.close()
    workbook.close()

if __name__ == '__main__':
    main()



