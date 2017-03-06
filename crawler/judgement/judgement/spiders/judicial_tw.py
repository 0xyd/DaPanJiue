# -*- coding: utf-8 -*-
import re
import time
import urllib
import scrapy
from datetime import datetime, timedelta
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError


class JudicialTwSpider(scrapy.Spider):
	name = "judicial_tw"
	log  = open('crawl_judge_tw.txt', 'a')
	allowed_domains = ["http://jirs.judicial.gov.tw/Index.htm"]
	start_urls = ['http://jirs.judicial.gov.tw/']

	headers = {
		'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'
	}

	judgement_query_url = 'http://jirs.judicial.gov.tw/FJUD/'
	judgement_list_referer = 'http://jirs.judicial.gov.tw/FJUD/FJUDQRY01_1.aspx'
	judgement_list_url = 'FJUDQRY02_1.aspx'
	judgement_item_referer = 'http://jirs.judicial.gov.tw/FJUD/FJUDQRY02_1.aspx'
	judgement_item_url = 'FJUDQRY03_1.aspx'

	# url="FJUDQRY02_1.aspx?&v_court=TPH+%e8%87%ba%e7%81%a3%e9%ab%98%e7%ad%89%e6%b3%95%e9%99%a2&v_sys=M&jud_year=105&jud_case=%e6%8a%97&jud_no=1&jud_no_end=100000&jud_title=&keyword=&sdate=20160101&edate=20161231&page=2&searchkw=&jmain=&cw=0"

	court_table = {
		'0': 'TPC 司法院－刑事補償',
		'1': 'TPS 最高法院',
		'2': 'TPH 臺灣高等法院',
		'3': 'IPC 智慧財產法院',
		'4': 'TCH 臺灣高等法院 臺中分院',
		'5': 'TNH 臺灣高等法院 臺南分院',
		'6': 'KSH 臺灣高等法院 高雄分院',
		'7': 'HLH 臺灣高等法院 花蓮分院',
		'8': 'TPD 臺灣臺北地方法院',
		'9': 'SLD 臺灣士林地方法院',
		'10' : 'PCD 臺灣新北地方法院',
		'11' : 'ILD 臺灣宜蘭地方法院',
		'12' : 'KLD 臺灣基隆地方法院',
		'13' : 'TYD 臺灣桃園地方法院',
		'14' : 'SCD 臺灣新竹地方法院',
		'15' : 'MLD 臺灣苗栗地方法院',
		'16' : 'TCD 臺灣臺中地方法院',
		'17' : 'CHD 臺灣彰化地方法院',
		'18' : 'NTD 臺灣南投地方法院',
		'19' : 'ULD 臺灣雲林地方法院',
		'20' : 'CYD 臺灣嘉義地方法院',
		'21' : 'TND 臺灣臺南地方法院',
		'22' : 'KSD 臺灣高雄地方法院',
		'23' : 'HLD 臺灣花蓮地方法院',
		'24' : 'TTD 臺灣臺東地方法院',
		'25' : 'PTD 臺灣屏東地方法院',
		'26' : 'PHD 臺灣澎湖地方法院',
		'27' : 'KMH 福建高等法院金門分院',
		'28' : 'KMD 福建金門地方法院',
		'29' : 'LCD 福建連江地方法院'
	}

	verdict_sys_table = {
		'M': '刑事',
		'V': '民事',
		'A': '行政',
		'P': '公懲',
	}

	# Y.D. 20170302: 
	vertict_number_re = re.compile('共\s*(?P<number>\d+)\s*筆')

	def gen_time_query(self, start_time, end_time):

		end_time   = [ end_time.year, end_time.month, end_time.day ]
		start_time = [ start_time.year, start_time.month, start_time.day ]

		end_date_q   = 'edate=' + \
			''.join([ str(et) if et > 10 else '0'+str(et) for et in end_time ])
		start_date_q = 'sdate=' + \
			''.join([ str(st) if st > 10 else '0'+str(st) for st in start_time ])

		return start_date_q + '&' + end_date_q

	def start_requests(self):

		# list_urls = ['http://jirs.judicial.gov.tw/FJUD/FJUDQRY02_1.aspx?sdate=20160101&jud_title=&keyword=&jmain=&searchkw=&v_court=PCD+%E8%87%BA%E7%81%A3%E6%96%B0%E5%8C%97%E5%9C%B0%E6%96%B9%E6%B3%95%E9%99%A2&edate=20161231&jud_year=&v_sys=M']
		list_urls = []
		courts = self.court_table.items()
		verdict_sys = self.verdict_sys_table.items()

		for court_code, court_name in courts:

			query = {
				'v_court': court_name,
				'jmain': '',
				'keyword': '',
				'searchkw': '',
				'jud_year': '',
				'jud_title': ''
			}

			for sys_code, sys_name in verdict_sys:
				query['v_sys'] = sys_code
				
				start_time = datetime(year=2016, month=1,  day=1)
				end_time   = datetime(year=2016, month=12, day=31)
				day_delta  = timedelta(days=1)

				while start_time < end_time:
					time_query = self.gen_time_query(start_time, start_time+day_delta)
					start_time = start_time + day_delta
					list_urls.append(
						self.judgement_query_url + self.judgement_list_url + '?' + urllib.parse.urlencode(query) + '&' + time_query)

		self.headers['Origin']  = 'http://jirs.judicial.gov.tw'
		self.headers['Referer'] = self.judgement_list_referer
		self.log.write('========== Start Crawling TW Verdicts ==========')

		for url in list_urls:
			self.log.write('')
			time.sleep(3)
			yield scrapy.Request(url=url, headers=self.headers, callback=self.parse_verdicts)


	def parse_verdicts(self, response):

		judge_meta = {}

		if response.status == 200:

			verdict_number_string = \
				response.css('#Form1 table:nth-child(5) table:first-child tr:first-child td font')[0].extract()
			verdict_number = self.vertict_number_re.search(verdict_number_string).group('number')
			verdict_url = response.url.replace('FJUDQRY02_1', 'FJUDQRY03_1')
			
			for id_num in range(1, int(verdict_number)):

				verdict_url = verdict_url + '&' + urllib.parse.urlencode({'id': id_num}) + '&cw=0'

				self.headers['Host'] = 'jirs.judicial.gov.tw'
				self.headers['Referer'] = self.judgement_item_referer

				time.sleep(1)
				yield scrapy.Request(
					url=verdict_url, headers=self.headers, 
					callback=self.parse_verdict, meta=judge_meta, errback=self.error_callback, dont_filter=True)
	

	# Y.D. 20170226: Select a verdict and its meta in row
	# def select_row_in_list(self, elements, index, css_rule):
	# 	try:
	# 		result = elements[index].css(css_rule)[0].extract()
	# 	except IndexError:
	# 		return 0
	# 	return result

	def parse_verdict(self, response):

		print('check response url:')
		print(response.url)

		if response.status == (200 or 302):

			# print('check context:')
			print(response.status)
			
			# print(response.meta)
			# response['meta']['context'] = response.body

			# return response['m
			pass 

			# yield {  }
		pass


	def parse_history(self, response):
		pass


	def error_callback(self, failure):
		if failure.check(HttpError):
			print(failure.value.response)
		elif failure.check(DNSLookupError):
			print(failure.request)
		elif failure.check(TimeoutError, TCPTimedOutError):
			print(failure.request)


