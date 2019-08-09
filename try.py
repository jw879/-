import pandas as pd
import numpy as np
import re
import requests
from bs4 import BeautifulSoup
import io
import sys
import csv
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')


#通过pandas提取list文件里的邮编
df = pd.read_csv('list.csv')
df = df.loc[: , 'postcode']
postcode = np.array(df)
postcode = postcode.tolist()
#print (postcode)

#伪装用户登录
url = "https://gbr.youbianku.com/postcode/"
kv = {'user-agent':'Mozilla/5.0'}

#循环搜索邮编并提取地址信息存入info_list
count = 0
address_list = []
info_list = []
for i in range(5):
	page = url + postcode[i]
	r = requests.get(page, headers = kv, timeout = 30)
	html = r.text
	soup = BeautifulSoup(html, 'html.parser')
	add = soup.find('title').string
	count = count +1
	address_list.append(add)

for i in range(len(address_list)):
	info_list.append([address_list[i]])
#print (info_list)

#写入csv
with open('address.csv', 'w', encoding = 'utf-8') as csvfile:
	spamwriter = csv.writer(csvfile, dialect='excel')
	#spamwriter.writerow(["address"])
	spamwriter.writerows(info_list)

print ("success!")
