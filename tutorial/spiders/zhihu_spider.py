#coding:utf-8
from scrapy.spider import Spider
from scrapy.selector import Selector
from tutorial.items import question_link, answer
from scrapy.http import Request, HtmlResponse
import sys
import urllib2
reload(sys)
sys.setdefaultencoding('utf-8')


class ZhihuSpider(Spider):
	name = 'Zhihu'
	#allowed_domains = 'zhihu.com'
	def __init__(self, username = None):
		self.start_urls = ['http://www.zhihu.com/people/' + str(username) + '/answers']

	def parse(self, response):  
		item = question_link()
		sel = Selector(response)
		next_link = sel.xpath(u'//span/a[text()="下一页"]/@href').extract()
		if next_link:
			next_link = self.start_urls[0] + next_link[0] 
			yield Request(url = next_link, callback = self.parse)

		for link in sel.xpath('//a[@class="question_link"]/@href').extract():
			yield Request(url = 'http://www.zhihu.com' + link, callback = self.parse_answer)

	
	def parse_answer(self, response):
		ans_item = answer()
		response_selector = Selector(response)
		ans_item['question'] = response_selector.xpath('//title[1]/text()').extract()
		ans_item['answer'] = response_selector.xpath('//div[@class = " zm-editable-content clearfix"][1]/text()').extract()
		yield ans_item