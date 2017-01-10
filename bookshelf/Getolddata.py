#! usr/bin/env python3
#--*--coding:utf8--*--

'''
Get all the information on the shelf
'''

import requests
from lxml import etree
from collections import defaultdict
#from bs4 import BeautifulSoup

def getqidiandata():
	headers = {'Cookie':(''),
				'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}
	url = 'http://t.qidian.com/BookCase/BookCase.php?caseId=-100'
	req = requests.Session().get(url, headers=headers)
	#bsobj = BeautifulSoup(req.text,'lxml')
	html = etree.HTML(req.text)
	leng = len(html.xpath('//tbody[@id="tbBookList"]/*')) + 1
	d = defaultdict(list)
	for n in range(1, leng):
		result1 = html.xpath('//tbody[@id="tbBookList"]/tr[%s]/td[3]/*[last()-3<=position()<=last()]' % n) #bookname, latest chapter
		result2 = html.xpath('//tbody[@id="tbBookList"]/tr[%s]/td[3]/*[position()=last()-1]/@href' % n) #book url
		result3 = html.xpath('//tbody[@id="tbBookList"]/tr[%s]/td[5]/a/@title' % n) or [None]	#bookmark
		x = [x.text for x in result1 if x.text != None][-2:] + result2 + result3
		d[x[0]] = x[:]
	return d