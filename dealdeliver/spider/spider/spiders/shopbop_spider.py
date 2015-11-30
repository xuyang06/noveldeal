import scrapy
from scrapy.selector import Selector
from scrapy.http import Request
from spider.items import ProductItem
import logging
import os
from datetime import datetime

logging.basicConfig(filename = os.path.join(os.getcwd(), 'log.txt'), level = logging.DEBUG, format = '%(asctime)s - %(levelname)s: %(message)s')  


def form_url(num, pre_str, after_str):
	return  pre_str + str(num*40) + after_str
	#return 'http://www1.bloomingdales.com/shop/sale/women/Pageindex,Sortby/' + str(num) + ',ORIGINAL?id=3985&cm_sp=categorysplash_sale_sale_1-_-row4_image_n-_-n'

def form_urls():
	page_num = 225;
	#page_num = 5;
	urls = []
	#pre_str_1 = 'http://shop.nordstrom.com/c/all-womens-sale?sort=Featured&page='
	pre_str_1 = 'https://www.shopbop.com/shop-category-sale/br/v=1/2534374302025763.htm?baseIndex='
	#after_str_1 = '?id=1003304&cm_sp=NAVIGATION-_-TOP_NAV-_-3977-SALE-%26-CLEARANCE-All-Sale-%26-Clearance'
	after_str_1 = ''
	for num in range(0, page_num):
		url1 = form_url(num, pre_str_1, after_str_1)
		urls.append(url1)
	return urls
	#http://www1.bloomingdales.com/shop/sale/all-sale-clearance/Pageindex/100?id=1003304&cm_sp=NAVIGATION-_-TOP_NAV-_-3977-SALE-%26-CLEARANCE-All-Sale-%26-Clearance
	#http://shop.nordstrom.com/c/all-womens-sale?sort=Featured&page=1
	
	
class ShopbopSpider(scrapy.Spider):
	name = "shopbop"
	allowed_domains = ["shopbop.com"]
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
		#products = sel.xpath('//a[@id="productTemplateId"]/@href').extract()
		#products = set(products)
		log = logging.getLogger('root')
		#log.debug('parsing products page %s, the page has total %s products ...', response.url, str(len(products)))
		#for product in products:
		#	product = 'http://www.neimanmarcus.com' + product
		#	log.debug('fetching No. %s product page ...', str(NeimanSpider.total_fetch_page))
		#	log.debug('fetch product_url: %s', product)
		#	NeimanSpider.total_fetch_page += 1
		#	yield Request(product, callback=self.parse_product)
		hrefs = sel.xpath('//a[@class=" url"]/@href').extract()
		images = sel.xpath('//img[@class="image thumbnail"]/@src').extract()
		brands = sel.xpath('//div[@class="brand"]/text()').extract()
		products = sel.xpath('//div[@class="title"]/text()').extract()
		pre_prices = sel.xpath('//span[@class="retail-price"]/text()').extract()
		sale_prices_low = sel.xpath('//span[@class="sale-price-low"]/text()').extract()
		sale_prices_high = sel.xpath('//span[@class="sale-price-high"]/text()').extract()
		log.debug('parsing products page %s, the page has total %s products ...', response.url, str(len(hrefs)))
		log.debug('the page has total %s images ...', str(len(images)))
		for i in range(len(hrefs)):
			item = ProductItem()
			item['time'] = str(self.dt.year) + '-' + str(self.dt.month) + '-' + str(self.dt.day) + '-' + str(self.dt.hour)
			item['site'] = 'shopbop.com'
			item['brand'] = brands[i].strip()
			item['image'] = images[i].strip()
			#item['image'] = ''
			#href = 'http://shop.nordstrom.com' + hrefs[i].strip()
			item['href'] = 'http://www.shopbop.com' + hrefs[i].strip()
			item['product'] = products[i].strip()
			#item['product'] = ''
			item['pre_price'] = pre_prices[i].strip()
			item['sale_price'] = sale_prices_low[i].strip() + ' ' + sale_prices_high[i].strip()
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