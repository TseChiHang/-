import numpy as np
import pandas as pd
import re
cities = pd.read_csv('省市区县2.csv',encoding='GBK',header=None,index_col=None)
cities=np.array(cities)
length=len(cities)
def slot_match_0(text):
    global final_slot
    global city
    global county
    global r1
    final_slot =None
    city=None
    county=None
    slot1="中高风险地区"
    slot2="防疫政策"
    slot3="没有问题"
    r1 = 0
    if(re.search(slot1,text)):

        for i in range(length):
            item=str(cities[i][0])
            if(re.search(item,text)!=None):
                for j in cities[i]:
                    if(((re.search(str(j),text)!=None)and str(j)!=item )or((re.search(str(j),text)!=None) and item == str(cities[i][1]))):
                        city=item
                        county=str(j)
                        r1=1
                        final_slot = slot1

    elif(re.search(slot2,text)!=None):
        for i in range(length):
            item=str(cities[i][0])
            if(re.search(item,text)!=None):
                city=item
                county=None
                r1=1
                final_slot = slot2
    elif(re.search(slot3,text)!=None):
        city=None
        county = None
        r1 = 1
        final_slot = slot3

    return bool(r1), city ,county ,final_slot

def slot_match_1(text):
    global final_slot
    global city
    global r1
    final_slot =None
    city=None
    slot1="中高风险地区"
    slot2="防疫政策"
    slot3="没有问题"
    r1 = 0
    if(re.search(slot1,text)):

        for i in range(length):
            item=str(cities[i][0])
            if(re.search(item,text)!=None):
                city=item
                r1=1
                final_slot = slot1

    elif(re.search(slot2,text)!=None):
        for i in range(length):
            item=str(cities[i][0])
            if(re.search(item,text)!=None):
                city=item
                r1=1
                final_slot = slot2
    elif(re.search(slot3,text)!=None):
        city=None
        r1 = 1
        final_slot = slot3

    return bool(r1), city ,final_slot
