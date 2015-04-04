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
	def __init__(self):
		self.user = 'cogito'
		self.start_urls = ['http://www.zhihu.com/people/' + self.user + '/answers']

	def parse(self, response):  
		item = question_link()
		sel = Selector(response)
		print 'hehe'
		for link in sel.xpath('//a[@class="question_link"]/@href').extract():
			print link
			yield Request(url = 'http://www.zhihu.com' + link, callback = self.parse_answer)

	
	def parse_answer(self, response):
		ans_item = answer()
		response_selector = Selector(response)
		ans_item['question'] = response_selector.xpath('//title[1]/text()').extract()
		ans_item['answer'] = response_selector.xpath('//div[@class = " zm-editable-content clearfix"][1]/text()').extract()
		yield ans_item




