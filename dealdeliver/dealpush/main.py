'''
Created on Sep 3, 2015

@author: xuyan_000
'''

from sendemail import send_email
from query import query
from account import account
import pymongo
#from query import ProductQuery

def notify_user(deal_query, user_email, user_name):
    query_res = deal_query.query_id_items(user_email)
    if len(query_res) != 0:
        user_email_list = [user_email]
        print user_email_list
        mail_content = send_email.write_mail_content(query_res, user_name)
        send_email.send_mail(user_email_list, "Notice from Novel Deal", mail_content)

def initialize():
    deal_query = query.DealQuery()
    db = account.Account()
    for user in db.get_user_list():
        #user_id = user[0]
        user_email = user[1]
        user_name = user[2]
    #for receiver_id,binding_keys in db.get_user_interests():
        notify_user(deal_query, user_email, user_name)

if __name__ == '__main__':
    initialize()