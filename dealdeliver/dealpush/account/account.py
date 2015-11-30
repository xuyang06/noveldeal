'''
Created on Sep 8, 2015

@author: xuyan_000
'''

#import pymongo
#from bson.objectid import ObjectId
#from pymongo.objectid import ObjectId
import MySQLdb

class Account():
    def __init__(self):
        host = 
        user = 
        passwd = 
        db = 
        self.conn=MySQLdb.connect(host=host, port=3306, user=user, passwd=passwd, db=db)
        self.cur = self.conn.cursor()
        #self.cursor.execute("create table if not exists user(id int primary key auto_increment, name varchar(255), password varchar(255), email varchar(255))")
        #self.cursor.execute("create table if not exists product(id int primary key auto_increment, brand varchar(255), category varchar(255), userid int)")
        #self.cur.execute('create table uprelation(id int not null auto_increment, userid int, productid int, primary key(id) if not exists ')
        
        #con = pymongo.MongoClient('localhost', 27017)
        #db = con['account']
        #self.collection = db['account']
    
    def get_insert_user_str(self, name, password, email):
        return "insert into user (id, name, password, email) values (null, '" + name + "', '" + password + "', '" + email + "')"
    
    def get_insert_product_str(self, brand, category, userid):
        return "insert into product (id, brand, category, userid) values (null, '" + brand + "', '" + category + "','" + str(userid) + "')"
    
    def get_user_str(self, email, password):
        return "select * from user where email='" + email + "' and password='" + password + "'"
    
    def get_user_list_str(self):
        return "select id, email, name from user"
    
    def get_user_account_str(self, email):
        return "select id from user where email='" + email + "'"
    
    def get_product_exist_str(self, brand, category, userid):
        return "select id from product where userid='" + str(userid) + "' and brand='" + brand + "' and category='" + category + "'"
    
    def get_product_str(self, userid):
        return "select id, brand, category from product where userid='" + str(userid) + "'"
    
    def get_update_user_account_str(self, email, password, id):
        return "update product set email='" + email +"',password='" + password + "' where id='" + str(id) + "'"
    
    def get_update_product_str(self, brand, category, id):
        return "update product set brand='" + brand +"',category='" + category + "' where id='" + str(id) + "'"
    
    def get_delete_product_str(self, brand, category, userid):
        return "delete from product where brand='" + brand +"' and category='" + category + "' and userid='" + str(userid) + "'"
    
    def get_delete_user_str(self, id):
        return "delete from user where id='" + str(id) + "'"
    
    def product_exist(self, brand, category, userid):
        get_product_exist_str = self.get_product_exist_str(brand, category, userid)
        self.cur.execute(get_product_exist_str)
        self.conn.commit()
        rows = self.cur.fetchall()
        return len(rows) > 0
    
    
    def delete_product(self, brand, category, userid):
        get_delete_product_str = self.get_delete_product_str(brand, category, userid)
        self.cur.execute(get_delete_product_str)
        self.conn.commit()
    
    def delete_user(self, id):
        get_delete_user_str = self.get_delete_user_str(id)
        self.cur.execute(get_delete_user_str)
        self.conn.commit()
    
    #def get_product
    
    def insert_product(self, brand, category, userid):
        if not self.product_exist(brand, category, userid):
            get_insert_product_str = self.get_insert_product_str( brand, category, userid)
            self.cur.execute(get_insert_product_str)
            self.conn.commit()
        
    def update_product(self, brand, category, productid):
        get_update_product_str = self.get_update_product_str(brand, category, productid)
        self.cur.execute(get_update_product_str)
        self.conn.commit()
            
    
    def insert_user_account(self, name, password, email):
        get_insert_user_str = self.get_insert_user_str(name, password, email)
        self.cur.execute(get_insert_user_str)
        self.conn.commit()
        #return self.get_user_account(email, password)
    
    def get_user_account(self, user_email, user_passwd):
        get_user_str = self.get_user_str(user_email, user_passwd)
        self.cur.execute(get_user_str)
        self.conn.commit()
        rows = self.cur.fetchall()
        if len(rows) == 0:
            return None
        return rows[0][0], rows[0][1]
    
    def get_user_list(self):
        get_user_list_str = self.get_user_list_str()
        self.cur.execute(get_user_list_str)
        self.conn.commit()
        rows = self.cur.fetchall()
        return rows
        
        
    def user_exist(self, user_email):
        get_user_account_str = self.get_user_account_str(user_email)
        self.cur.execute(get_user_account_str)
        self.conn.commit()
        rows = self.cur.fetchall()
        return len(rows) > 0
    
    
    
    def get_user_interest(self, id):
        get_product_str = self.get_product_str(id)
        self.cur.execute(get_product_str)
        self.conn.commit()
        rows = self.cur.fetchall()
        return rows
    
        
    
    #def get_user_email(self, id):    
    #    cursor = self.collection.find({'_id':ObjectId(id)})
    #    if cursor.count() == 0:
    #        return None
    #    return cursor[0]['user_email']
    
    
    
    #def update_user_interest(self, user_id, interests = []):
        
    #    self.collection.update_one({'_id':user_id}, {'$set':{'interesting_brand':interests}})
        
    
    #def update_user_brands(self, user_name, user_passwd, user_email, interesting_brand=[]):
    #    self.collection.update_one({'user_name':user_name, 'user_passwd':user_passwd, 'user_email':user_email}, {'$set':{'interesting_brand':interesting_brand}}, upsert=True)
    
    #def update_user_passwd(self, user_name, user_passwd, user_email, interesting_brand=[]):
    #    self.collection.update_one({'user_name':user_name, 'interesting_brand':interesting_brand, 'user_email':user_email}, {'$set':{'user_passwd':user_passwd}}, upsert=True)
    
    #def update_user_email(self, user_name, user_passwd, user_email, interesting_brand=[]):
    #    self.collection.update_one({'user_name':user_name, 'interesting_brand':interesting_brand, 'user_passwd':user_passwd}, {'$set':{'user_email':user_email}}, upsert=True)
    
    #def get_user_interests(self):
    #    #user_interests = {}
    #    cursor = self.collection.find()
    #    for doc in cursor:
    #        yield doc['_id'], doc['interesting_brand']
    
    def stop(self):
        self.cursor.close()
        self.conn.close()
    
    
if __name__ == '__main__':
    account = Account()
    name = "yong xu" 
    password = "myufo" 
    email = "xuyang06@gmail.com"
    #rows = account.insert_user_account(name, password, email)
    #print rows
    
    exist = account.user_exist('xuyang06@gmail.com')
    print exist
    brand = "Parada"
    category = "shoes"
    #account.insert_product(brand, category, 1)
    #brand = "Prada"
    #category = "shoes"
    #account.insert_product(brand, category, 1)
    #category = "clothes"
    #account.update_product(brand, category, 3)
    #account.delete_product(2)
    #account.delete_user(2)
    #user_name = 'Yang Xu'
    #user_passwd = '1234'
    #user_email = 'xuyang06@gmail.com'
    #interesting_brand = ['Prada']
    #print account.get_user_interest(1)
    print account.get_user_account(email, password)
    #account.update_user_brands(user_name, user_passwd, user_email, interesting_brand)