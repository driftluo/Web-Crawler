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
			except:
				print(sys.exc_info())
			finally:
				self.conn.commit()

	def updatanewchapter(self, dic):
		'''
		dic.value structure [latestchapter, updatetime, bookname]
		'''
		for v in dic.values():
			try:
				self.cur.execute('updata bookinformation set latestchapter=%s updatatime=%s where bookname=%s', tuple(v))
			except:
				print(sys.exc_info()[0])
			finally:
				self.conn.commit()
		self.close()

	def updatabookmark(self, dic):
		'''
		dic.value structure [bookmark, bookname]
		'''
		for v in dic.values():
			try:
				self.cur.execute('updata bookinformation set bookmark=%s where bookname=%s', tuple(v))
			except:
				print(sys.exc_info()[0])
			finally:
				self.conn.commit()
		self.close()

	def delebook(self, dic):
		'''
		dic.value structure [bookname]
		'''
		for v in dic.values:
			try:
				self.cur.execute('delete from bookinformation where bookname=%s', tuple(v))
			except:
				print(sys.exc_info()[0])
			finally:
				self.conn.commit()
		self.close()

	def close(self):
		self.cur.close()
		self.conn.close()