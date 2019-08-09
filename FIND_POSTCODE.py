import pandas as pd
import numpy as np
import re
import requests
from bs4 import BeautifulSoup
import io
import sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')

df = pd.read_csv('list.csv')
df = df.loc[: , 'postcode']
postcode = np.array(df)
postcode = postcode.tolist()



kv = {'user-agent':'Mozilla/5.0'}
def getHTML(url):
	try:
		r = requests.get(page, headers = kv, timeout = 30)
		r.raise_for_status
		return r.text
	except:
		return "gg1"

def parsePage(info_list, html):
		address_list = []
		soup = BeautifulSoup(demo, 'html.parser')
		add = soup.find('title').string
		address_list.append(add)
		for i in range(len(postcode)):
			info_list.append([address_list[i]])
		return info_list



def printList(list):
	file_name = 'G:\\project\\address.csv'
	headers = ['address']
	data = pd.DataFrame(columns = headers, data = list)
	data.to_csv(file_name)

def main():
	url = "https://gbr.youbianku.com/postcode/"
	info_list = []
	for i in range(len(postcode)):
		page = url + postcode[i]
		demo = getHTML(page)
		list = parsePage(info_list, demo)
	printList(list)

main()





