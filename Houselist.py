import requests
import io
import sys
from bs4 import BeautifulSoup
import re
import csv
import numpy
import pandas as pd

sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')

def getHTMLText(url):
	try:
		r = requests.get(url, timeout = 30)
		r.raise_for_status
		return r.text
	except:
		return "gg1"

def parsePage(info_list, html):
	try:
		price_list = []
		type_list = []
		SaleTime_list = []
		Bedroom_list = []
		address_list = []
		tp_list=[]#type类型：detached，semi-detached, flat
		tenure_list=[]#产权类型：leasehold, freehold

		soup = BeautifulSoup(html, 'html.parser')
		[s.extract() for s in soup('span')]

		count = 0
		for addres in soup.select('div.soldDetails'):
			a = addres.find( attrs = 'soldAddress').string
			address_list.append(a)

			#再选中所有最后一次售卖的信息
			info = addres.find_all('tr', attrs={'class': False})
			for trtag in info:
				sp = trtag.find('td', 'soldPrice').string
				price_list.append(sp)

				st = trtag.find('td', 'soldType').string
				type_list.append(st)
				a = re.split( ',' , st)[0]#提取房屋类
				tp_list.append(a)
				b = re.split( ',' , st)[1]#提取产权类型
				tenure_list.append(b)


				sd = trtag.find('td', 'soldDate').string
				SaleTime_list.append(sd)

				nb = trtag.find('td', 'noBed').string
				Bedroom_list.append(nb)

		for i in range(len(address_list)):
			info_list.append([address_list[i], price_list[i], tp_list[i], tenure_list[i], SaleTime_list[i], Bedroom_list[i]])
		return info_list
	except:
		print ('gg2')


def printHouseList(list):
	file_name = 'G:\\project\\HouseList.csv'
	headers = ['address', 'price', 'houseType', 'tenure','SaleTime', 'Bedroom']
	data = pd.DataFrame(columns = headers, data = list)
	data.to_csv(file_name)


def main():
	depth = 40
	start_url = 'https://www.rightmove.co.uk/house-prices/Cardiff.html?country=england&locationIdentifier=REGION%5E281&searchLocation=Cardiff'
	info_list = []
	for i in range(depth):
		url = start_url + '&index=' + str(25*i)
		html = getHTMLText(url)
		list = parsePage(info_list, html)
	printHouseList(list)

main()
