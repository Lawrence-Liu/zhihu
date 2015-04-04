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
			#haha = Request(url = 'http://www.zhihu.com' + link, callback = self.parse_answer)
			# body = urllib2.urlopen(url = 'http://www.zhihu.com' + link).read()
			# response = HtmlResponse(url = 'http://www.zhihu.com' + link, body = body)
			# self.parse_answer(response)
		# # for site in sites:
		# # 	item = question_link()
		# # 	item.link = site.xpath('a/@href').extract()
		# # 	items.append(item)
		# filename = response.url.split("/")[-2]  
		# with open(filename, 'wb') as f:
		# 	f.write(items)
	
	def parse_answer(self, response):
		ans_item = answer()
		response_selector = Selector(response)
		ans_item['answer'] = response_selector.xpath('//div[@class = " zm-editable-content clearfix"][1]').extract()
		ans_item['question'] = response_selector.xpath('//title[1]').extract()
		yield ans_item




