# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json

class TutorialPipeline(object):
	def __init__(self):
		self.file = open('items.jl', 'wb')

	def process_item(self, item, spider):
		line = json.dumps(dict(item), encoding = 'utf-8', ensure_ascii=False) + "\n" 
		self.file.write(line)


# class TopicPipeline(object):
# 	def __init__(self):
# 		self.file = open('topic.jl', 'wb')

# 	def