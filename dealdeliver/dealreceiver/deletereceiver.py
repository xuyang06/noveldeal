'''
Created on Sep 12, 2015

@author: xuyan_000
'''

import multiprocessing
from sets import Set
import redis
import os
import signal

def terminate():
    _redis = redis.StrictRedis(host='localhost', port=6379, db=0)
    pid = _redis.spop('processes')
    while pid != None:
        #print pid
	#while True:
        try:
            os.kill(int(pid), signal.SIGTERM)
        except OSError as err:
            print err
        pid = _redis.spop('processes')
            #break
    #processes = ReceiverProcesses()

if __name__ == '__main__':
    terminate()
