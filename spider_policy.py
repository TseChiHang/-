# -*- coding:utf-8 -*-

import re

import requests


def grab_strategy(ans=''):

    print("请输入您想查询的城市拼音缩写：\n","友情提示，当存在拼音缩写相同时可以试试打出全名，例如：\n","福州：fz\n","抚州：fuzhou")
    ans=input(ans)

    url = "http://m.nj.bendibao.com/news/gelizhengce/all.php?leavecity=" +ans+ "&leavequ=&qu=&src=baidu"
   # print(url)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.55"
    }
    # 以字典的形式设置请求头，处理反爬
    resp = requests.get(url, headers=headers)
    #print(resp.status_code)
    resp = resp.text.replace('\u200b', '')
    #print(resp)
    #alert = re.findall("hspace=(.+?)align=", resp,flags=16)
    blert = re.findall("Alert\\(\`(.+?)\"", resp, flags=16)
    #print(alert)
    blert=str(blert)
    blert=blert.replace("\\r\\n","")
    blert = blert.replace("`", "")
    blert = blert.replace("')", "'")

    print(blert)


if __name__ == '__main__':
    grab_strategy()