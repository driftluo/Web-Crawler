#! usr/bin/env python3
#--*--coding:utf8--*--

'''
data store、updata、delete
'''

import pymysql
import sys

class OperationData:
	def __init__(self, db, port=3306, host='localhost', user='root', passwd='system', charset='utf8'):
		self.conn = pymysql.connect(host=host, user=user, passwd=passwd, db=db, port=port, charset=charset)
		self.cur = self.conn.cursor()

	def insert(self, dic):
		'''
		dic.value structure [bookname, latestchapter, url, bookmark]
		'''
		for v in dic.values():
			try:
				self.cur.execute('insert into bookinformation (bookname, latestchapter, url, bookmark) value(%s,%s,%s,%s)', tuple(v))
				print('insert %s' % v[0])
			except:
				print(sys.exc_info())
			finally:
				self.conn.commit()
		self.close()

	def updatenewchapter(self, dic):
		'''
		dic.value structure [latestchapter, updatetime, bookname]
		'''
		for v in dic.values():
			try:
				self.cur.execute('update bookinformation set latestchapter=%s updatetime=%s where bookname=%s', tuple(v))
				print('update newchapter %s, time is %s, bookname is %s' % tuple(v))
			except:
				print(sys.exc_info())
			finally:
				self.conn.commit()
		self.close()

	def updatebookmark(self, dic):
		'''
		dic.value structure [bookmark, bookname]
		'''
		for v in dic.values():
			try:
				self.cur.execute('update bookinformation set bookmark=%s where bookname=%s', tuple(v))
				print('update mark %s, bookname is %s' % tuple(v))
			except:
				print(sys.exc_info())
			finally:
				self.conn.commit()
		self.close()

	def delebook(self, dic):
		'''
		dic.value structure [bookname]
		'''
		for v in dic.values():
			try:
				self.cur.execute('delete from bookinformation where bookname=%s', tuple(v))
				print('delete book %s' % tuple(v))
			except:
				print(sys.exc_info())
			finally:
				self.conn.commit()
		self.close()

	def updateurl(self, dic):
		'''
		dic.value structure [url, bookname]
		'''
		for v in dic.values():
			try:
				self.cur.execute('update bookinformation set url=%s where bookname=%s', tuple(v))
				print('update url=%s,bookname is %s' % tuple(v))
			except:
				print(sys.exc_info())
			finally:
				self.conn.commit()
		self.close()

	def close(self):
		self.cur.close()
		self.conn.close()