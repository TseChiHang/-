import requests
from bs4 import BeautifulSoup
import pandas as pd



class getArea():
    def __init__(self):
        self.baseInfoSet()

    def baseInfoSet(self):
        self.mainPage_url = 'https://zh.m.wikipedia.org/zh-hans/%E4%B8%AD%E5%8D%8E%E4%BA%BA%E6%B0%91%E5%85%B1%E5%92%8C%E5%9B%BD%E8%A1%8C%E6%94%BF%E5%8C%BA%E5%88%92'
        self.base_url = 'https://zh.m.wikipedia.org/'

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
        }

        # 设置代理隧道
        self.proxy_host = 'http-short.xiaoxiangdaili.com'
        self.proxy_port = 10010
        self.proxy_username = '880049792682971136'
        self.proxy_pwd = 'u2turrEH'

        self.proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
            "host": self.proxy_host,
            "port": self.proxy_port,
            "user": self.proxy_username,
            "pass": self.proxy_pwd,
        }

        self.proxies = {
            'http': self.proxyMeta,
            'https': self.proxyMeta,
        }

        self.specialArea = ['上海市','北京市', '天津市','上海市', '香港特别行政区', '澳门特别行政区', '台湾省']

        self.failedGetNum = 0  # 获取失败的个数
        self.failedGetName = []  # 获取失败的名称

        self.provinceAndCity = [[],[]]  # 前一个填省份，后一个对应市



    def getProvCityProcess(self):
        '''
        获取省份和市
        :return:
        '''
        province_href = self.getProvince()
        print(province_href)
        for province in province_href:
            provName = province[0]
            provUrl = province[1]
            if provName in self.specialArea:
                continue
            print('开始爬取{}'.format(provName))
            self.getCity(provName, provUrl)
            print('{}爬取完毕'.format(provName))

        column = ['省份','市']
        data = dict(zip(column, self.provinceAndCity))
        data_pd = pd.DataFrame(data)
        data_pd.to_csv('省市.csv', encoding='utf_8_sig', index=False)

    def getResponse(self, url):
        '''
        根据网页链接获取响应
        :param url:
        :return: 返回响应内容
        '''

        try:
            s = requests.session()
            s.keep_alive = False
            response = requests.get(url, headers=self.headers, timeout=10)
            print(f'网页响应码：{response.status_code}')
            if response.status_code == 200:
                return response
            else:
                print('网页响应失败！')
                return False
        except Exception as e:
            print('网页请求失败，发生异常：{}'.format(e))
            return False


    def getProvince(self):
        '''
        解析主页面，获取并返回个省份及其链接
        :return:
        '''

        province_href = []

        mainPage_response = self.getResponse(self.mainPage_url)
        if mainPage_response == False:
            print('主网页获取失败')
        else:
            print('开始查找主页面的目标表格')
            mainPage_soup = BeautifulSoup(mainPage_response.text, 'lxml')
            table_tags = mainPage_soup.select('table[class="wikitable"]')
            for tag in table_tags:
                cap = tag.select('caption')
                if cap and ('分省统计的省级以下行政区划' in cap[0].string):
                    print('找到目标表格，开始解析')
                    tr_tags = tag.select('tr')[3:]

                    for tr in tr_tags:
                        a_tag = tr.select('a')
                        provName = a_tag[0].string
                        provUrl = self.base_url + a_tag[0].attrs['href']
                        province_href.append((provName, provUrl))
                    print('表格解析完成')
                    break
            else:
                print('未找到目标表格')

        return province_href


    def getCity(self, provName, provUrl):
        '''
        获取省份下面的市及其链接
        :param provName:
        :param provUrl:
        :return:
        '''
        city_href = []

        prov_response = self.getResponse(provUrl)
        if prov_response == False:
            print('{}网页获取失败'.format(provName))
            self.failedGetNum += 1
            self.failedGetName.append(provName)
        else:
            print('开始查找{}的目标表格'.format(provName))
            prov_soup = BeautifulSoup(prov_response.text, 'lxml')
            table_tags = prov_soup.select('table[class="wikitable"]')
            for tag in table_tags :
                b = tag.select('b')
                if b and ('行政区划' in b[0].string):
                    print('找到目标表格，开始解析')
                    tr_tags = tag.select('tr')[4:]
                    for tr in  tr_tags:
                        a_tag = tr.select('th a')
                        if a_tag:
                            name = a_tag[0].string
                            href = self.base_url + a_tag[0].attrs['href']
                            city_href.append((name, href))
                            self.provinceAndCity[0].append(provName)
                            self.provinceAndCity[1].append(name)
                    print('表格解析完成')
                    break
            else:
                print('未找到目标表格')

        return city_href


    def getTown(self, cityName, cityUrl):
        '''
        获取城市下的区县
        :param cityName:
        :param cityUrl:
        :return:
        '''
        town = []

        city_response = self.getResponse(cityUrl)
        if city_response == False:
            print('{}网页获取失败'.format(cityName))
            self.failedGetNum += 1
            self.failedGetName.append(cityName)
        else:
            print('开始查找{}的目标表格'.format(cityName))
            city_soup = BeautifulSoup(city_response.text, 'lxml')
            table_tags = city_soup.select('table[class="wikitable"]')
            for tag in table_tags:
                th_tags= tag.select('th')
                if th_tags and ('行政区' in th[0].string):
                    print('找到目标表格，开始解析')
                    tr_tags = tag.select('tr')[4:]
                    for tr in tr_tags:
                        th = tr.select('th')
                        if th:
                            town.append(th[1].string)
                    print('表格解析完成')
                    break
            else:
                print('未找到目标表格')

        return town


    def getSpecialTown(self, cityName, cityUrl):
        '''
        获取北京等特殊城市下的区
        :param cityName:
        :param cityUrl:
        :return:
        '''
        town = []


if __name__ == '__main__':
    spiderAgent = getArea()
    spiderAgent.getProvCityProcess()

