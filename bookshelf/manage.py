#! usr/bin/env python3
#--*--coding:utf8--*--

import CrawlerData
import OperationData
import pymysql
import sys
import threading
import time

def displaydata():
	try:
		conn = pymysql.connect(host='localhost', user='root', passwd='system', db='example', port=3306, charset='utf8')
		cur = conn.cursor()
		cur.execute('select bookname, latestchapter, bookmark, updatetime, url from bookinformation where dr=0')
		datas = cur.fetchall()
	except:
		print(sys.exc_info())
	finally:
		cur.close()
		conn.close()
	return datas

def updateurl():
	a = CrawlerData.CrawlerData()
	b = OperationData.OperationData('example')
	conn = pymysql.connect(host='localhost', user='root', passwd='system', db='example', port=3306, charset='utf8')
	cur = conn.cursor()
	cur.execute('select bookname from bookinformation where dr=0 and url is null')
	datas = cur.fetchall()
	cur.close()
	conn.close()
	datas = [i[0] for i in list(datas)]
	a.urlupdate(datas)
	b.updateurl(a.urldic)

def deletebook(bookname):
	a = CrawlerData.CrawlerData()
	b = a.delbook(bookname)
	c = OperationData.OperationData('example')
	c.delebook(b)

def insertbook(bookname, latestchapter=None, url=None, bookmark=None):
	a = CrawlerData.CrawlerData()
	b = OperationData.OperationData('example')
	c = a.insertbook(bookname, latestchapter, url, bookmark)
	b.insert(c)

def manualmark(mark, bookname):
	a = CrawlerData.CrawlerData()
	b = OperationData.OperationData('example')
	c = a.manualmark(mark, bookname)
	#print(a.markdic)
	b.updatebookmark(a.markdic)

def updatenewchapter(maxthread=10):
	c = CrawlerData.CrawlerData()
	d = OperationData.OperationData('example')
	conn = pymysql.connect(host='localhost', user='root', passwd='system', db='example', port=3306, charset='utf8')
	cur = conn.cursor()
	num1 = cur.execute('select bookname from bookinformation where dr=0')
	num = cur.execute('select url, bookname from bookinformation where dr=0 and url is not null')
	if num < num1: updateurl()
	datas = cur.fetchall()
	cur.close()
	conn.close()
	datas = [list(i) for i in datas]
	for data in datas:
		data[0] = data[0] + '#Catalog'
		print(data)
		threads = []
		while  threads:
			for thread in threads:
				if not thread.is_alive():
					threads.remove(thread)
		while len(threads) < maxthread and data:
			thread = threading.Thread(target=c.newchapter, args=data)
			thread.setDaemon(True)
			thread.start()
			threads.append(thread)
		time.sleep(1)
	d.updatenewchapter(c.chapterdic)
		
updatenewchapter()