# -*- coding:utf-8 -*-
import re

import match
import spider_policy

def Run():
    result = True



    while (result):
        print('qs?')
        text = input()
        result, city, county, slot = match.slot_match_0(text)
        if (result == 2):
            city=city.replace("市",'')
            spider_policy.grab_strategy(city)
        elif(slot=="没有问题"):
            print("正常退出")

    return 0


