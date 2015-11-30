# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo

from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy import log
#from kafka import SimpleProducer, KafkaClient
#from spider.producerwrapper import ProducerWrapper
from spider.sender import Sender

class MongoDBPipeline(object):

	def __init__(self):
		client = pymongo.MongoClient(
			settings['MONGODB_SERVER'],
			settings['MONGODB_PORT']
		)
		db = client[settings['MONGODB_DB']]
		self.collection = db[settings['MONGODB_COLLECTION']]
		self.collection.drop()
		#self.kafka = KafkaClient('localhost:9092')
		#self.topic_consumer_dict = {}
		self.sender = Sender()
		
	def process_item(self, item, spider):
		valid = True
		for data in item:
			if not data:
				valid = False
				raise DropItem("Missing {0}!".format(data))
		if valid:
			update_res = self.collection.update_one({'brand':item['brand'], 'href':item['href'], 'product':item['product'], 'image':item['image'], 'site':item['site']}, {'$push':{'prices':{'pre_price':item['pre_price'],  'sale_price':item['sale_price'], 'time':item['time']}}}, upsert=True)
			if update_res.matched_count == 0:
				msg_str_dict = {'brand':item['brand'], 'href':item['href'], 'product':item['product'], 'image':item['image'], 'site':item['site'], 'pre_price':item['pre_price'], 'sale_price':item['sale_price']}
				self.sender.send_message(item['brand'], msg_str_dict)
				#if not self.topic_consumer_dict.has_key():
				#	self.topic_consumer_dict[item['brand']] = ProducerWrapper(self.kafka, item['brand'])
				#self.topic_consumer_dict[item['brand']].send_message(msg_str_dict)
			#self.collection.insert(dict(item))
            #log.msg("Question added to MongoDB database!",
            #        level=log.DEBUG, spider=spider)
		return item
	
	def __del__(self):
		self.sender.stop()
	


class SpiderPipeline(object):
	def process_item(self, item, spider):
		return item
