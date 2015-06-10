# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TutorialItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class question_link(scrapy.Item):
	link = scrapy.Field()
	
class answer(scrapy.Item):
	question = scrapy.Field()
	answer = scrapy.Field()
	upvote = scrapy.Field()
	#downvote = scrapy.Field()

