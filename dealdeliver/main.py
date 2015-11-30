# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
#!/usr/bin/env python
import os
import time
#class ProductItem(Item):
#	title = Field()
#	pre_price = Field()
#	sale_price = Field()
	
if __name__ == '__main__':
	#os.system("cd ~/spider")
	os.system("/usr/bin/python /home/yangxu/dealreceiver/createreceiver.py &")
	os.chdir("/home/yangxu/spider")
	os.system("/usr/local/bin/scrapy crawl shopbop")
	os.system("/usr/local/bin/scrapy crawl nordstorm")
	os.system("/usr/local/bin/scrapy crawl sakes")
	os.system("/usr/local/bin/scrapy crawl bluefly")
	os.system("/usr/bin/python /home/yangxu/dealpush/main.py")
	time.sleep(30)
	os.system("/usr/bin/python /home/yangxu/dealreceiver/deletereceiver.py")
