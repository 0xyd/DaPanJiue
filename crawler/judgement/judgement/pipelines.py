# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

class JudgementPipeline(object):

	def __init__(self):

		self.output = open('output.json', 'a')


    def process_item(self, item, spider):

		json.dump(item, self.output, ident=4)

        return item
