#coding:utf-8
from scrapy.spider import Spider
from scrapy.selector import Selector
from tutorial.items import question_link, answer
from scrapy.http import Request, HtmlResponse
import sys
import urllib2
reload(sys)
sys.setdefaultencoding('utf-8')

#todo: for now those text wrapped by any html tag is ignored. 
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
		ans_item['question'] = response_selector.xpath('//title[1]/node()').extract()
		ans_item['answer'] = ''.join(response_selector.xpath('//div[@class = " zm-editable-content clearfix"][1]/node()').extract())
		ans_item['upvote'] = response_selector.xpath('//div[@class="zm-item-vote-info "]/@data-votecount')[0].extract()
		ans_item['image_urls'] = response.xpath('//div[@class = " zm-editable-content clearfix"][1]/noscript/img/@src').extract()
		yield ans_item


class TopicSpider(ZhihuSpider):
	name = 'Topic'
	def __init__(self, topic = None):
		self.start_urls = ['http://www.zhihu.com/topic/' + str(topic) + '/top-answers']

	def parse(self, response):
		sel = Selector(response)
		next_link = sel.xpath(u'//span/a[text()="下一页"]/@href').extract()
		if next_link:
			next_link = self.start_urls[0] + next_link[0] 
			yield Request(url = next_link, callback = self.parse)

		for link in sel.xpath(u'//a[text()="显示全部"]/@href').extract():
			yield Request(url = 'http://www.zhihu.com' + link, callback = self.parse_answer)