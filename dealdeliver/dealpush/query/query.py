#import pymongo

#from scrapy.conf import settings
#from scrapy.exceptions import DropItem
#from scrapy import log

import redis
import cPickle
import locale
locale.setlocale(locale.LC_ALL, 'en_US.UTF8')

def get_price(str):
	strs = str.split()
	price = 0.0
	num = 0
	for item in strs:
		if '$' in item:
			price += float(locale.atof(item[1:])) 
			num += 1
	return price/num

def getKey(item):
	return item['off']


class DealQuery(object):
	
	def __init__(self):
		self._redis = redis.StrictRedis(host='localhost', port=6379, db=0)
	
	
	def query_id_items(self, user_id):
		query_res = []
		item = self._redis.spop(user_id)
		while item != None:
			item = cPickle.loads(item)
			sale_item = {}
			sale_item['brand'] = item['brand']
			sale_item['href'] = item['href']
			sale_item['product'] = item['product']
			pre_price = get_price(item['pre_price'])
			sale_price = get_price(item['sale_price'])
			sale_item['off'] = sale_price/pre_price
			query_res.append(sale_item)
			item = self._redis.spop(user_id)
		sorted(query_res, key=getKey)
		return query_res
		
# 	def query_item(self, brand, time, product=None):
# 		res = []
# 		if product is None:
# 			res = self.collection.find({'brand':brand})
# 		else:
# 			res = self.collection.find({'brand':brand, 'product':product})
# 		query_res = []
# 		for item in res:
# 			pre_price = None
# 			sale_price = None
# 			for price in item['prices']:
# 				if price['time'] == time:
# 					pre_price = price['pre_price']
# 					sale_price = price['sale_price']
# 					break
# 			if pre_price is not None:
# 				pre_price = self.get_price(pre_price)
# 				sale_price = self.get_price(sale_price)
# 				if pre_price*0.6 > sale_price:
# 					sale = {}
# 					sale['brand'] = item['brand']
# 					sale['href'] = item['href']
# 					sale['product'] = item['product']
# 					sale['pre_price'] = pre_price
# 					sale['sale_price'] = sale_price
# 					query_res.append(sale)
# 		return query_res
# 					
# 				
	
	
	
	
# if __name__ == "__main__":
# 	query = ProductQuery();
# 	brand = 'Prada'
# 	query_res = query.query_item(brand, '2015-9-3-16')
# 	print query_res
#     #app.run(host='0.0.0.0',port=5000,debug=True)		