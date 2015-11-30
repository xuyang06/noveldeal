# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import os

#class ProductItem(Item):
#	title = Field()
#	pre_price = Field()
#	sale_price = Field()
	
if __name__ == '__main__':
	#os.system("cd ~/spider")
	os.system("python /home/yangxu/dealreceiver/createreceiver.py &")
	os.system("scrapy crawl shopbop")
	os.system("scrapy crawl nordstorm")
	os.system("scrapy crawl sakes")
	os.system("scrapy crawl bluefly")
	os.system("python /home/yangxu/dealpush/main.py")
	os.system("python /home/yangxu/dealreceiver/deletereceiver.py")
