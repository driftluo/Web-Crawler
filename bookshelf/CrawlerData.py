#! usr/bin/env python3
#--*--coding:utf8--*--

import requests
from lxml import etree
import re
from collections import defaultdict
from selenium import webdriver
import time, sys, json

class CrawlerData:
	def __init__(self):
		self.chapterdic = defaultdict(list)
		self.markdic = defaultdict(list)
		self.urldic = defaultdict(list)
		self.headers = {'Cookie':(""),
				'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
				'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}
		self.url = 'http://t.qidian.com/BookCase/BookCase.php?caseId=-100'

	def newchapter(self, url, bookname):
		'''
		Gets asynchronously loaded json data, and then fetch the useful things
		'''
		try:
			self.req1 = requests.get(url, headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
												'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'})
			self.req1.encoding = 'utf-8'
			self.t_dict = json.loads(self.req1.text)
			self.t1 = self.t_dict['data']['vs'][-1]['cs'][-1]['uT']		# updatetime
			self.t2 = self.t_dict['data']['vs'][-1]['cs'][-1]['cN']		# newchapter
			self.chapterdic[bookname] = [self.t2]
			self.chapterdic[bookname].append(self.t1)
			self.chapterdic[bookname].append(bookname)
		except:
			print(sys.exc_info())
		
	def newmark(self):
		try:
			self.req2 = requests.Session().get(self.url, headers=self.headers).text
			self.html2 = etree.HTML(self.req2)
			self.leng = len(self.html2.xpath('//tbody[@id="tbBookList"]/*')) + 1
			for n in range(1, self.leng):
				self.mark = self.html2.xpath('//tbody[@id="tbBookList"]/tr[%s]/td[5]/a/@title' % n) or [None]
				self.bookname = self.html2.xpath('//tbody[@id="tbBookList"]/tr[%s]/td[3]/*[position()=last()-1]/text()' % n)
				if self.mark[0]:
					self.mark[0] = self.mark[0][5:]
				self.markdic[self.bookname[0]] = self.mark + self.bookname
		except:
			print(sys.exc_info())


	def manualmark(self, mark, bookname):
		self.markdic[bookname] = [mark, bookname]

	def urlupdate(self, booknames):
		self.driver = webdriver.PhantomJS(executable_path=r'E:\webdriver\phantomjs-2.1.1-windows\bin\phantomjs')
		self.driver.get('http://www.qidian.com')
		try:
			for bookname in booknames:
				self.driver.switch_to_window(self.driver.window_handles[0])
				self.driver.find_element_by_class_name("search-box").send_keys(bookname)
				self.driver.find_element_by_id("search-btn").click()
				self.driver.switch_to_window(self.driver.window_handles[-1])
				time.sleep(2)
				if self.driver.find_element_by_xpath('//*[@id="result-list"]/div/ul/li[1]/div[2]/h4/a').text == bookname:
					self.urldress = self.driver.find_element_by_xpath('//*[@id="result-list"]/div/ul/li[1]/div[2]/h4/a').get_attribute('href')
					self.urldic[bookname] = [self.urldress, bookname]
				self.driver.close()
		except:
			print(sys.exc_info())
		finally:
			for handle in self.driver.window_handles:
				self.driver.switch_to_window(handle)
				self.driver.close()

	def delbook(self, bookname):
		return {bookname:[bookname]} 

	def insertbook(self, bookname, latestchapter=None, url=None, bookmark=None):
		return {bookname:[bookname, latestchapter, url, bookmark]}
