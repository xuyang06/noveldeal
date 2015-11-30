import scrapy
from scrapy.selector import Selector
from scrapy.http import Request
from spider.items import ProductItem
import logging
import os
from datetime import datetime
logging.basicConfig(filename = os.path.join(os.getcwd(), 'log.txt'), level = logging.DEBUG, format = '%(asctime)s - %(levelname)s: %(message)s')  


def form_url(num, pre_str, after_str):
	return  pre_str + str(num) + after_str
	#return 'http://www1.bloomingdales.com/shop/sale/women/Pageindex,Sortby/' + str(num) + ',ORIGINAL?id=3985&cm_sp=categorysplash_sale_sale_1-_-row4_image_n-_-n'

def form_urls():
	page_num = 20;
	urls = []
	pre_str_1 = 'http://www.neimanmarcus.com/Sale/Shoes/cat46520731_cat980731_cat000000/c.cat#userConstrainedResults=true&refinements=&page='
	after_str_1 = '&pageSize=30&sort=PCS_SORT&definitionPath=/nm/commerce/pagedef_rwd/template/EndecaDrivenHome&onlineOnly=&allStoresInput=false&rwd=true&catalogId=cat46520731'
	pre_str_2 = 'http://www.neimanmarcus.com/Sale/Handbags/cat46520737_cat980731_cat980731/c.cat#userConstrainedResults=true&refinements=&page='
	after_str_2 = '&pageSize=30&sort=PCS_SORT&definitionPath=/nm/commerce/pagedef_rwd/template/EndecaDrivenHome&locationInput=&radiusInput=100&onlineOnly=&allStoresInput=false&rwd=true&catalogId=cat46520737'
	for num in range(1, page_num + 1):
		url1 = form_url(num, pre_str_1, after_str_1)
		urls.append(url1)
	for num in range(1, page_num + 1):
		url2 = form_url(num, pre_str_2, after_str_2)
		urls.append(url2)
	return urls

class NeimanSpider(scrapy.Spider):
	name = "neiman"
	allowed_domains = ["neimanmarcus.com"]
	#start_urls = [
	#	"http://www1.bloomingdales.com/shop/sale/women?id=3985&cm_sp=categorysplash_sale_sale_1-_-row4_image_n-_-n"
	#]
	start_urls = form_urls()
	dt = datetime.now()
	total_parse_page = 1
	total_fetch_page = 1
	#def parse(self, response):
	#	print "response"
	#	filename = response.url.split("/")
	#	filename = filename[-2]
		#filename = filename[-1].split(".")[-2]
	#	print filename
	#	with open(filename, 'wb') as f:
	#		f.write(response.body)
	
	
	#	for sel in response.xpath('//ul/li'):
	#		title = sel.xpath('a/text()').extract()
	#		link = sel.xpath('a/@href').extract()
	#		desc = sel.xpath('text()').extract()
	#		print title, link, desc
	
	#def parse(self, response):
		#items = []
		#sel = Selector(response) 
		#page_num = int(sel.xpath('//div[@id="row_101_2"]/ul/li/div/div/ul/li[@class="lastPage"]/text()').extract()[0])
		#log = logging.getLogger('root')
		#log.debug('total page_num: %s', str(page_num))
		#for num in range(1, page_num):
		#	url = self.form_url(num)
		#	log.debug('fetch page_url: %s', url)
			#print url
		#	yield Request(url, callback=self.parse_products)
	#	return self.parse_products(response)
		
	
	#def parse_products(self, response):
	
	
	def parse(self, response):
		#items = response.meta['items']
		sel = Selector(response)
		products = sel.xpath('//a[@id="productTemplateId"]/@href').extract()
		#products = set(products)
		log = logging.getLogger('root')
		log.debug('parsing products page %s, the page has total %s products ...', response.url, str(len(products)))
		#for product in products:
		#	product = 'http://www.neimanmarcus.com' + product
		#	log.debug('fetching No. %s product page ...', str(NeimanSpider.total_fetch_page))
		#	log.debug('fetch product_url: %s', product)
		#	NeimanSpider.total_fetch_page += 1
		#	yield Request(product, callback=self.parse_product)
		hrefs = sel.xpath('//div[@class="productdesigner OneLinkNoTx"]/a[@class="recordTextLink"]/@href').extract()
		brands = sel.xpath('//div[@class="productdesigner OneLinkNoTx"]/a[@class="recordTextLink"]/text()').extract()
		products = sel.xpath('//div[@class="productname hasdesigner OneLinkNoTx"]/a[@class="recordTextLink"]/text()').extract()
		pre_prices = sel.xpath('//p[@class="price-adornment priceadorn strikethrough"]/span[@class="price OneLinkNoTx"]/text()').extract()
		sale_prices = sel.xpath('//p[@class="price-adornment priceadorn price-adornment-highlight "]/span[@class="price OneLinkNoTx"]/text()').extract()
		for i in range(len(hrefs)):
			item = ProductItem()
			item['site'] = 'neimanmarcus.com'
			item['brand'] = brands[i].strip().lower()
			item['image'] = ''
			item['href'] = hrefs[i].strip()
			item['product'] = products[i].strip().lower()
			item['pre_price'] = pre_prices[i].strip()
			item['sale_price'] = sale_prices[i].strip()
			item['time'] = str(self.dt.year) + '-' + str(self.dt.month) + '-' + str(self.dt.day) + '-' + str(self.dt.hour)
			yield item
		
	
	#def parse_product(self, response):
		#items = response.meta['items']
	#	sel = Selector(response)
	#	log = logging.getLogger('root')
	#	log.debug('parsing No. %s product page ...', str(NeimanSpider.total_parse_page))
	#	log.debug('parsing product page %s ...', response.url)
	#	title = sel.xpath('//span[@tabindex="0"]/text()').extract()[0].strip()
	#	pre_price = sel.xpath('//span[@class="item-price"]/text()').extract()[0].strip()
		#old_price = float(pre_prices[0].strip()[1:])
		#sale_price = float(sel.xpath('//span[@class="priceSale"]/text()').extract()[0].strip()[5:])
		#pre_price = pre_prices[0].strip()
	#	sale_price = sel.xpath('//span[@class="pos1override item-price"]/text()').extract()[0].strip()
	#	item = ProductItem()
	#	item['title'] = title
	#	item['pre_price'] = pre_price
	#	item['sale_price'] = sale_price
	#	NeimanSpider.total_parse_page += 1
	#	yield item
	
	
	
	
	
	
	#def parse(self, response):
		#items = response.meta['items']
	#	sel = Selector(response)
	#	products = sel.xpath('//a[@id="productTemplateId"]/@href').extract()
	#	products = set(products)
	#	log = logging.getLogger('root')
	#	log.debug('parsing products page %s, the page has total %s products ...', response.url, str(len(products)))
	#	for product in products:
	#		product = 'http://www.neimanmarcus.com' + product
	#		log.debug('fetching No. %s product page ...', str(NeimanSpider.total_fetch_page))
	#		log.debug('fetch product_url: %s', product)
	#		NeimanSpider.total_fetch_page += 1
	#		yield Request(product, callback=self.parse_product)
	
	#def parse_product(self, response):
		#items = response.meta['items']
	#	sel = Selector(response)
	#	log = logging.getLogger('root')
	#	log.debug('parsing No. %s product page ...', str(NeimanSpider.total_parse_page))
	#	log.debug('parsing product page %s ...', response.url)
	#	title = sel.xpath('//span[@tabindex="0"]/text()').extract()[0].strip()
	#	pre_price = sel.xpath('//span[@class="item-price"]/text()').extract()[0].strip()
		#old_price = float(pre_prices[0].strip()[1:])
		#sale_price = float(sel.xpath('//span[@class="priceSale"]/text()').extract()[0].strip()[5:])
		#pre_price = pre_prices[0].strip()
	#	sale_price = sel.xpath('//span[@class="pos1override item-price"]/text()').extract()[0].strip()
	#	item = ProductItem()
	#	item['title'] = title
	#	item['pre_price'] = pre_price
	#	item['sale_price'] = sale_price
	#	NeimanSpider.total_parse_page += 1
	#	yield item
		
		
	#def form_url(self, num):
	#	return 'http://www1.bloomingdales.com/shop/sale/women/Pageindex,Sortby/' + str(num) + ',ORIGINAL?id=3985&cm_sp=categorysplash_sale_sale_1-_-row4_image_n-_-n'
		
		
	#	products = response.xpath('//a[contains(@href, "www1.bloomingdales.com/shop/product")]/@href')
	#	for product in products:
	#		yield Request(product, callback=self.parse_product)
	
		
	#	yield Request(url, meta={'item': item}, callback=self.parse_item)
		
	#	sites = sel.xpath('//a[contains(@href)]')
	#	links = response.xpath('//a/@href')
	#	links = response.xpath('//a[contains(@href, "www1.bloomingdales.com/shop/product")]/@href')
		
	#	links = response.xpath('//div[@id="row_101_2"]/ul/li/div/ul/li/div/div/a')
		
	#	page_num = response.xpath('//div[@id="row_101_2"]/ul/li/div/div/ul/li[@class="lastPage"]')
		
	#	http://www1.bloomingdales.com/shop/sale/women/Pageindex,Sortby/6,ORIGINAL?id=3985&cm_sp=categorysplash_sale_sale_1-_-row4_image_n-_-n
		
    #   sites = sel.xpath('//ul/li')  
    #    for site in sites:  
    #        title = site.xpath('a/text()').extract()  
    #        link = site.xpath('a/@href').extract()  
    #        desc = site.xpath('text()').extract()  
    #        print title  
		#for href in response.css("ul.directory.dir-col > li > a::attr('href')"):
		#	url = response.urljoin(href.extract())
		#	yield scrapy.Request(url, callback=self.parse_dir_contents)
		
	#	http://www1.bloomingdales.com/shop/product/ella-moss-dress-cortez-off-the-shoulder-maxi?ID=1364974&CategoryID=3985&LinkType=#fn=spp%3D2%26ppp%3D96%26sp%3D6%26rid%3D%26spc%3D6608%26pn%3D1
		
	#	title = response.xpath('//h1[@id="productTitle"]/text()')
		
	#	pre_prices = response.xpath('//span[@class="priceBig"]/text()')
	#	sale_price = response.xpath('//span[@class="priceSale"]/text()')
		
		
	#def parse_dir_contents(self, response):
	#	for sel in response.xpath('//ul/li'):
	#		item = DmozItem()
	#		item['title'] = sel.xpath('a/text()').extract()
	#		item['link'] = sel.xpath('a/@href').extract()
	#		item['desc'] = sel.xpath('text()').extract()
	#		yield item
	
	
	#def parse(self, response):
    #    for sel in response.xpath('//ul/li'):
    #        title = sel.xpath('a/text()').extract()
    #        link = sel.xpath('a/@href').extract()
    #        desc = sel.xpath('text()').extract()
    #        print title, link, desc