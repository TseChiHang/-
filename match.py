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
                for j in range(1,len(cities[i])):
                    if(re.search(str(cities[i][j]),text)!=None):
                        city=item
                        county=cities[i][j]
                        r1=1
                        final_slot = slot1

    elif(re.search(slot2,text)!=None):
        for i in range(length):
            item=str(cities[i][0])
            if(re.search(item,text)!=None):
                city=item
                county=None
                r1=2
                final_slot = slot2
    elif(re.search(slot3,text)!=None):
        city=None
        county = None
        final_slot = slot3

    return r1, city ,county ,final_slot

def slot_match_1(text):
    global final_slot
    global city
    global r1
    final_slot =None
    city=None
    district=None
    slot1="中高风险地区"
    slot2="防疫政策"
    slot3="没有问题"
    r1 = 0
    if(re.search(slot1,text)):

        for i in range(length):
            item=str(cities[i][0])
            if(re.search(item,text)!=None ):
                city=item
                r1=1
                final_slot = slot1

    elif(re.search(slot2,text)!=None):
        for i in range(length):
            item=str(cities[i][0])
            if(re.search(item,text)!=None):
                city=item
                r1=2
                final_slot = slot2
    elif(re.search(slot3,text)!=None):
        city=None
        r1 = 0
        final_slot = slot3

    return r1, city ,final_slot

