import requests
from bs4 import BeautifulSoup
import re




def grab_region(city):
    url = "https://www.haoyunbb.com/news/pne_fx_00.html"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.55"
    }  # 以字典的形式设置请求头，处理反爬
    resp = requests.get(url, headers=headers)
    #print(resp)  # 结果：<Response [200]>
    resp = resp.text.replace('\xa0', '')       # 拿到页面源代码'''
    html=resp
    #print(resp)

    high = re.findall("<li class='w70'>" + str(city) + "：(.+?)高风险</li>", resp)
    if (high):
       for i in range(0,len(high)):
            print(city+"的高风险地区：")
            high[i] = re.findall("(.+?)</li>", high[i])
            print(high[i])
    else:
        print(city+"没有高风险地区。")
    mid = re.findall("<li class='w70'>" + str(city) + "：(.+?)中风险</li>", resp)
    if (mid):
       for j in range(0,len(mid)):
            print(city + "的中风险地区：")
            mid[j] = re.findall("(.+?)</li>", mid[j])
            print(mid[j])
    else:
        print(city+"没有中风险地区。")


#grab_region("福州市")




def grab_strategy(city):
    url = "http://m.nj.bendibao.com/news/gelizhengce/all.php?leavecity="+city+"&leavequ=&qu=&src=baidu"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.55"
    }
    # 以字典的形式设置请求头，处理反爬
    resp = requests.get(url, headers=headers)
    resp = resp.text.replace('\u200b', '')
    print(resp)
    alert=re.findall()

grab_strategy("zjk")