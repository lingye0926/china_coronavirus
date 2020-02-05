#coding:utf-8
import requests
import lxml
from bs4 import BeautifulSoup
import json
import pandas as pd
import re
import datetime

list1 = []
url = 'https://3g.dxy.cn/newh5/view/pneumonia'
headers = {'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}

response = requests.get(url,headers=headers)
response.encoding = 'utf-8'
rawresult = re.search(
        '<script id="getAreaStat">(.*)</script>', response.text)
provincedata = re.search(
        '\[.*\]', rawresult.group(1)).group(0).split('catch')
finalresult = provincedata[0]
finalresult = finalresult[0:-1]
# print(finalresult)
jsondata = json.loads(finalresult)
# print(jsondata)

# soup = BeautifulSoup(res.content,'lxml')
# province_data = soup.find_all(id = 'getAreaStat')[0]
# data = province_data.get_text(strip=True)
# virus_data = '\''+data[27:-11]+'\''
# json_doc = json.loads(virus_data)
# print(json_doc)
list2 = []
list_city = []
# print(json_doc['provinceName'])
print(jsondata[0]['confirmedCount'])
provinceNum = 0
for provinceNum in range(0,34):
    provinceName = jsondata[provinceNum]['provinceName']
    provinceShortName = jsondata[provinceNum]['provinceShortName']
    confirmedCount = jsondata[provinceNum]['confirmedCount']
    suspectedCount = jsondata[provinceNum]['suspectedCount']
    curedCount = jsondata[provinceNum]['curedCount']
    deadCount = jsondata[provinceNum]['deadCount']
    comment = jsondata[provinceNum]['comment']
    date = datetime.date.today()
    list1 = [provinceName,provinceShortName,confirmedCount,suspectedCount,curedCount,deadCount,comment,date]
    # print(list1)
    for cityNum in range(0,str(jsondata[provinceNum]['cities']).count('cityName')):
        try:
            province = jsondata[provinceNum]['provinceName']
            cityName = jsondata[provinceNum]['cities'][cityNum]['cityName']
            confirmedCount = jsondata[provinceNum]['cities'][cityNum]['confirmedCount']
            suspectedCount = jsondata[provinceNum]['cities'][cityNum]['suspectedCount']
            curedCount = jsondata[provinceNum]['cities'][cityNum]['curedCount']
            deadCount = jsondata[provinceNum]['cities'][cityNum]['deadCount']
            date = datetime.date.today()
            list3 = [province,cityName,confirmedCount,suspectedCount,curedCount,deadCount,date]
            list_city.append(list3)
        except IndexError:
            continue
    # cities = jsondata[provinceNum]['cities']
       
    list2.append(list1)
# print(list2)
today = datetime.date.today()
df1 =pd.DataFrame(list2)
df2 = pd.DataFrame(list_city)
df1.columns=['provinceName','provinceShortName','confirmedCount','suspectedCount','curedCount','deadCount','comment','date']
# df1.to_csv(r'/Users/lye/Documents/图表小挑战/武汉冠状病毒疫情/各省疫情数据.csv',encoding='utf_8_sig')
df2.columns = ['provinceName','cityName','confirmedCount','suspectedCount','curedCount','deadCount','date']
# df2.to_csv(r'/Users/lye/Documents/图表小挑战/武汉冠状病毒疫情/各城市详细疫情.csv',encoding='utf_8_sig')
with pd.ExcelWriter(r'/Users/lye/Documents/图表小挑战/武汉冠状病毒疫情/各省疫情数据'+ str(today) +'.xlsx') as writer:
    for i in range(1,3):
        name = 'Sheet_name_'+str(i)
        df1.to_excel(writer, sheet_name = '各省数据')
        df2.to_excel(writer, sheet_name = '各城市数据')
writer.save()
writer.close()