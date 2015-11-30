'''
Created on Sep 8, 2015

@author: xuyan_000
'''

from account import account
from receiver import receiver
import multiprocessing
from sets import Set
import redis
import os

def worker(receiver_id, binding_keys):
    #print str(receiver_id) + ' start'
    _redis = redis.StrictRedis(host='localhost', port=6379, db=0)
    _redis.sadd('processes', os.getpid())
    rec = receiver.Receiver(receiver_id, binding_keys)
    rec.process()
    
class ReceiverProcesses():
    
    def __init__(self):
        
        self.processes = []
        db = account.Account()
        for user in db.get_user_list():
            print user
            user_id = user[0]
            user_email = user[1]
            interests = db.get_user_interest(user_id)
            binding_keys = Set()
            for interest in interests:
                binding_keys.add(interest[1])
            p = multiprocessing.Process(target = worker, args = (user_email,binding_keys,))
            self.processes.append(p)
            p.start()
            #p.join()
    
    #def stop(self):
    #    for p in self.processes:
    #        p.terminate()


def initilize():
    _redis = redis.StrictRedis(host='localhost', port=6379, db=0)
    _redis.sadd('processes', os.getpid())
    processes = ReceiverProcesses()

if __name__ == '__main__':
    initilize()
    
#if __name__ == '__main__':
#    ReceiverProcesses = initilize()