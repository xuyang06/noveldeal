'''
Created on Sep 8, 2015

@author: xuyan_000
'''

from account import account
from receiver import receiver
import multiprocessing

def worker(receiver_id, binding_keys):
    print str(receiver_id) + ' start'
    rec = receiver.Receiver(receiver_id, binding_keys)
    rec.process()

if __name__ == '__main__':
    db = account.Account()
    for receiver_id,binding_keys in db.get_user_interests():
        p = multiprocessing.Process(target = worker, args = (receiver_id,binding_keys,))
        p.start()