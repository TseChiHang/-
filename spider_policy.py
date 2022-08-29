# -*- coding:utf-8 -*-

import re

import requests
from xpinyin import Pinyin

def grab_strategy(ans):

    #print("请输入您想查询的城市拼音缩写：\n","友情提示，当存在拼音缩写相同时可以试试打出全名，例如：\n","福州：fz\n","抚州：fuzhou")
    #ans=input(ans)
    n1=Pinyin()
    name=n1.get_pinyin(ans)
    name1=name.replace('-','')
    #print(name1)
    name2=name.split('-')
    #print(name2)
    name2="".join([i[0].lower()for i in name2])
    if(name2=="qqhe"):
        name2='qqhr'
    url_1= "http://m.nj.bendibao.com/news/gelizhengce/all.php?leavecity=" +name1+ "&leavequ=&qu=&src=baidu"
    url_2 = "http://m.nj.bendibao.com/news/gelizhengce/all.php?leavecity=" + name2 + "&leavequ=&qu=&src=baidu"
   # print(url)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.55"
    }
    # 以字典的形式设置请求头，处理反爬
    resp_1 = requests.get(url_1, headers=headers)
    resp_2 = requests.get(url_2, headers=headers)
    print(resp_2)
    #print(resp.status_code)
    resp_1= resp_1.text.replace('\u200b', '')
    resp_2=resp_2.text
    #print(resp)
    #alert = re.findall("hspace=(.+?)align=", resp,flags=16)
    alert = re.findall("Alert\\(\`(.+?)\"", resp_1, flags=16)
    blert = re.findall("Alert\\(\`(.+?)\"", resp_2, flags=16)
    #print(alert)
    alert=str(alert)
    alert=alert.replace("\\r\\n","")
    alert = alert.replace("`", "")
    alert = alert.replace("')", "'")
    blert = str(blert)
    blert = blert.replace("\\r\\n", "")
    blert = blert.replace("`", "")
    blert = blert.replace("')", "'")

    print("得到信息：")
    if(1 or re.search("nj.bendibao",resp_2)==None):
        print("检索" + "\"" + name1 + "\"：\n", alert)
    print("检索"+"\""+name2+"\"：\n",blert)
    print("可能会检索到拼音缩写相同的城市信息，请注意辨别")



if __name__ == '__main__':
    print("main")
    grab_strategy(input())