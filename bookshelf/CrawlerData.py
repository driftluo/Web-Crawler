#! usr/bin/env python3
#--*--coding:utf8--*--

import requests
from lxml import etree
import re
from collections import defaultdict
from selenium import webdriver
import time, sys

class CrawlerData:
	def __init__(self):
		self.chapterdic = defaultdict(list)
		self.markdic = defaultdict(list)
		self.urldic = defaultdict(list)
		self.headers = {'Cookie':("beacon_visit_count=5; _csrfToken=EBlhyPLbneML9uLOUQy4vtlCLk9hwmXEUanzMtD7; qg_ad_guid=ec9a66a5b272a4940ecd3c50a97fe118; "
						"pgv_pvi=8588560384; stat_gid=8229292493; qdgd=1; b_110128=0; nread=2; isBindWeiXin=0; vjuids=47ae19f09.158a97e7953.0.5d406d4a90f9e; "
						"__utma=1.805958954.1474686619.1481528100.1482167106.347; __utmz=1.1482167106.347.326.utmcsr=qidian.com|utmccn=(referral)|utmcmd=referral|utmcct=/; "
						"ns=2; nb=2; b_t_s=s; dltk=1%7Ck03476149; ad_gid=1483593317541155; mdltk=id=ad391ee26f9ce582e615aa1461f016b3&nk=%e9%80%8d%e9%81%a5%e5%ad%a4%e7%90%85&ut=2&si=7b832f2c0f08e1582c426d1bdf32eacc&pd=k03476149&hi=102&ai=d64353edfca01f3d1529e0a19eb82d2d&an=; "
						"qdrs=0|4|0|0|1; vjlast=1480312388.1483812216.11; stat_id24=0,-1,1,noimg; e1=%7B%22pid%22%3A%22qd_P_xianxia%22%2C%22eid%22%3A%22qd_A47%22%2C%22l1%22%3A40%7D; e2=%7B%22pid%22%3A%22qd_P_wuxia%22%2C%22eid%22%3A%22qd_A49%22%2C%22l1%22%3A40%7D; hiijack=0; "
						"ywkey=yw3660591706; ywguid=119190067553; al=1; cmfuToken=N((88dA53zMBH7Ak-9JUhY3zNRItDwYjaznzhMbp85yZX9OiY0_6x7BKF512_OnbqwRi1PmhhN68Lgme-rbjmuMMQEbqteEYLiEaqovmf_p90RDXrfmCYK7_YBXkvrYb1PkeTwbvZEteGcpM4-LMiRuZou9q5-d1mf9qrOVvHz7yCwR5u04RJjEiIyuJtIqQ8c9"
						"rdrWite8swSoAhI6wXNJSSmcNZ6F92Sjw0CQmQvVs9D05zUiZO8_lWwhlDSh067U9W8LbUANboieRpXTY75v7FXYwhYJAligDkv08z9EEkHSWzDbWqN_AY9lUNzEjfUzE1Hc0GJ-wv7WwOMuyi3A1XLGCNzHEBT3UZ9DoYKSyeg1; qduid=9771921; stat_sessid=19085527390; lrbc=1003636531%7C348545983%7C1; "
						"rcr=1003636531%2C1003680825%2C1004947907%2C1004438356%2C1003578985%2C1003307568%2C1004181718%2C1003448414%2C3547101%2C1003565884%2C3516230%2C1003790747%2C1004120651%2C1004200296%2C1003312190%2C3557673%2C1003763471%2C3544073%2C1003698302%2C1004175378"
						"%2C1004137713%2C1003506219%2C1003900126%2C1003663290%2C1003422010%2C1003742515%2C1003801025%2C3650892%2C1003631173%2C3663825%2C1004837400%2C1004821173%2C1003504656%2C3681932%2C1003736111%2C1001756434%2C1003902251%2C1003634299"),
				'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
				'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}
		self.url = 'http://t.qidian.com/BookCase/BookCase.php?caseId=-100'

	def newchapter(self, url, bookname):
		try:
			self.req1 = requests.get(url, headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
												'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}).text
			self.html1 = etree.HTML(self.req1)
			print(self.req1)
			self.uptime = self.html1.xpath('//div[@class="volume"]') #updatetime
			print(self.uptime)
			self.chaptername = self.html1.xpath('//div[@class="volume"][position()=last()]/ul/li[position()=last()]/a/text()') #chaptername
			self.uptime = re.findall('\d{4}-\d{2}-\d{2}.{,2}\d{2}:\d{2}:\d{2}', self.uptime[0])
			self.chapterdic[bookname] = self.chaptername + self.uptime
			self.chapterdic[bookname].append(bookname)
		except:
			print(sys.exc_info(), self.uptime, bookname)
		
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
