# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field

#class ProductItem(Item):
#	title = Field()
#	pre_price = Field()
#	sale_price = Field()
	
class ProductItem(Item):
	brand = Field()
	product = Field()
	pre_price = Field()
	sale_price = Field()
	href = Field()
	site = Field()
	time = Field()
	image = Field()

class SpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
