# -*- coding:utf-8 -*-
import re
import requests
from bs4 import BeautifulSoup
import pandas as pd

import match
import spider_policy


def getResponse(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.55"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        code = response.status_code
        # print('网页响应码：{}'.format(code))
        if code == 200:
            # print()
            return response
        else:
            print('网页响应错误：{}'.format(code))

    except Exception as e:
        print('网页请求失败：{}'.format(e))
        return False


def searchACTown(province, city, town):
    '''
    输入省份，城市，区县，获取该地区的疫情信息
    :param province:
    :param city:
    :param town:
    :return:
    '''
    main_url = "https://www.haoyunbb.com/news/pne_fx_00.html"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.55"
    }
    base_url = 'https://www.haoyunbb.com'
    specialCity = ['北京', '北京市', '上海', '上海市', '天津', '天津市', '重庆', '重庆市']
    specialProv = {'内蒙古自治区':'内蒙古','广西壮族自治区':'广西','西藏自治区':'西藏','宁夏回族自治区':'宁夏',
                   '新疆维吾尔自治区':'新疆'}

    if province in specialProv.keys():
        province = specialProv[province]

    mainPage_response = getResponse(main_url)

    if mainPage_response:
        mainPage_soup = BeautifulSoup(mainPage_response.text, 'lxml')

        prov_tags = mainPage_soup.select('ul[class="fxdj"] li')[4:]
        for i in range(0, len(prov_tags), 2):
            prov_name = prov_tags[i].select('a')[0].string
            pro_simple = province[:-1] if (('省' in province) or ('市' in province)) else province
            if pro_simple in prov_name:
                b_tags = prov_tags[i + 1].select('b')
                if b_tags == []:
                    print(f'{province}无中高风险地区')
                else:
                    degree = ''
                    for b in b_tags:
                        if '低' in b.string:
                            continue
                        degree = degree + b.string + ' '
                    print('{}的风险等级有：{}'.format(province, degree))
                    print('其中所查区域范围内的风险地区有：')
                    prov_url = base_url + prov_tags[i].select('a')[0].attrs['href']

                    prov_response = getResponse(prov_url)
                    if prov_response:
                        prov_soup = BeautifulSoup(prov_response.text, 'lxml')
                        if prov_soup.select('ul[class="fxarea"] li') == []:
                            print('暂无相关数据')
                            return
                        detailInfo_tags = prov_soup.select('ul[class="fxarea"] li')[2:]
                        area_num = 0
                        flag = (city in specialCity)
                        for j in range(0, len(detailInfo_tags), 2):
                            area = detailInfo_tags[j].string
                            if ((city in area) or flag) and (town in area):

                                deg = detailInfo_tags[j + 1].string
                                if deg == '低风险':
                                    continue
                                area_num += 1
                                print('{}地区: {}'.format(deg, area))
                        if area_num == 0:
                            print('您所查询的地区没有疫情')
                        else:
                            print('共查询出{}条数据'.format(area_num))

                break



        else:
            print('查无此省，请检查是否输入正确的省份')


def LocateProvWithCity(city):
    '''
    根据城市定位省份
    :param city:
    :return:
    '''
    province = ''
    specialCity = ['北京', '北京市', '上海', '上海市', '天津', '天津市', '重庆', '重庆市']
    if city in specialCity:
        province = city
    else:
        data_pd = pd.read_csv('省市.csv')
        city_simple = city.replace('市','')
        target = data_pd[data_pd['市'].str.find(city_simple) != -1]
        prov = list(target['省份'])
        if prov:
            province = prov[0]
            print('{}位于{}'.format(city, province))
        else:
            print('查无此市，请检查是否输入正确')
    return province




def Run():
    result = True



    while (result):
        print('qs?')
        text = input()
        result, city, county, slot = match.slot_match_0(text)
        print('result={}'.format(result))
        print('city={}'.format(city))
        print('county={}'.format(county))
        print('slot={}'.format(slot))
        if (result == 2):
            spider_policy.grab_strategy()
        elif result == 1:
            print('开始查询')
            province = LocateProvWithCity(city)
            searchACTown(province, city, county)


    return 0






if __name__ == '__main__':

    Run()

