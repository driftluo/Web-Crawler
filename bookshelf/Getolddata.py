#! usr/bin/env python3
#--*--coding:utf8--*--

'''
Get all the information on the shelf
'''

import requests
from lxml import etree
from collections import defaultdict
import time
import json
#from bs4 import BeautifulSoup


def getqidiandata():
    headers = {'Cookie': (),
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}
    url = 'http://my.qidian.com/ajax/BookShelf/BookList?_csrfToken=EBlhyPLbneML9uLOUQy4vtlCLk9hwmXEUanzMtD7&pageIndex=1&pageSize=100&sort=0&c=&gid=-100'
    req = requests.Session().get(url, headers=headers)
    #bsobj = BeautifulSoup(req.text,'lxml')
    req.encoding = 'utf-8'
    data = json.loads(req.text)
    data = data['data']['listInfo']
	for n in range(len(data)-1):
		self.mark = [self.data[n]['readCname']]
		self.bookname = [self.data[n]['bName']]
		self.markdic[self.bookname[0]] = self.mark + self.bookname
    return data

print(getqidiandata())
