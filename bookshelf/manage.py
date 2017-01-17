#! usr/bin/env python3
#--*--coding:utf8--*--

'''
manage Crawler and Operation
'''

import CrawlerData
import OperationData
import pymysql
import sys
import threading
import time

def displaydata():
	'''
	fetch all data from local shelf
	'''
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
	'''
	Query the data is missing url, add in
	'''
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
	'''
	Manually delete book
	'''
	a = CrawlerData.CrawlerData()
	b = a.delbook(bookname)
	c = OperationData.OperationData('example')
	c.delebook(b)

def insertbook(bookname, latestchapter=None, url=None, bookmark=None):
	'''
	Manually add new book
	'''
	a = CrawlerData.CrawlerData()
	b = OperationData.OperationData('example')
	c = a.insertbook(bookname, latestchapter, url, bookmark)
	b.insert(c)

def manualmark(mark, bookname):
	'''
	Manually update new mark
	'''
	a = CrawlerData.CrawlerData()
	b = OperationData.OperationData('example')
	c = a.manualmark(mark, bookname)
	#print(a.markdic)
	b.updatebookmark(a.markdic)

def updatenewchapter():
	'''
	scrawl new chapter each book, and then update it
	'''
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
	threads = []
	for data in datas:
		data[0] = data[0].replace('http://book.qidian.com/info/',
					'http://book.qidian.com/ajax/book/category?_csrfToken=EBlhyPLbneML9uLOUQy4vtlCLk9hwmXEUanzMtD7&bookId=')
		print(data)
		thread = threading.Thread(target=c.newchapter, args=data)
		threads.append(thread)
		thread.start()
		time.sleep(0.25)
	for thread in threads:
		thread.join()
	d.updatenewchapter(c.chapterdic)
		
def updatenewmark():
	'''
	scrawl new mark each book on network shelf, and then update it
	'''
	e = CrawlerData.CrawlerData()
	f = OperationData.OperationData('example')
	e.newmark()
	f.updatebookmark(e.markdic)

def insertnewbook():
	'''
	scrawl new book on network shelf, insert it
	'''
	a = CrawlerData.CrawlerData()
	b = OperationData.OperationData('example')
	a.newmark()
	t = set(a.markdic.keys())
	conn = pymysql.connect(host='localhost', user='root', passwd='system', db='example', port=3306, charset='utf8')
	cur = conn.cursor()
	cur.execute('select bookname from bookinformation where dr=0')
	res = cur.fetchall()
	k = set([i[0] for i in list(res)])
	j = t - k
	for i in j:
		insertbook(i)
		print('new book %s' %i)

if __name__ == '__main__':
	if len(sys.argv) < 2 and len(sys.argv) > 3:
		print('see doc to help')
	elif len(sys.argv) == 2 and sys.argv[1] == 'update':
		insertnewbook()
		updatenewmark()
		updatenewchapter() 
		print('update finish')
	elif len(sys.argv) == 2 and sys.argv[1] == 'delete':
		name = input('要删除的书名：')
		name = name.strip()
		deletebook(name)
	elif len(sys.argv) == 2 and sys.argv[1] == 'insert':
		name = input('要增加的书名：')
		name = name.strip()
		insertbook(name)
	elif len(sys.argv) == 2 and sys.argv[1] == 'mark':
		name = input('书名：')
		chapter = input('章节名：')
		name = name.strip()
		chapter = chapter.strip()
		manualmark(chapter, name)