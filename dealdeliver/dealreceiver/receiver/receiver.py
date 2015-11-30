'''
Created on Sep 7, 2015

@author: xuyan_000
'''
import pika
import sys
import cPickle
import redis

#kafka_server=['localhost:9092']
#topic_list = ['prada']

def topic_fill(top_str):
    new_str = ''
    for c in top_str:
        if (c >= 'a' and c <= 'z') or (c >= 'A' and c <= 'Z'):
            new_str += c.lower()
    return new_str


class Receiver(object):
    
    def __init__(self, receiver_id, binding_keys):
        self.receiver_id = receiver_id
        self._redis = redis.StrictRedis(host='localhost', port=6379, db=0)
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange='topic_news', type='topic')
        result = self.channel.queue_declare(exclusive=True)
        self.queue_name = result.method.queue
        for binding_key in binding_keys:
            binding_key = '#.' + topic_fill(binding_key) + '.#'
            self.channel.queue_bind(exchange='topic_news', queue=self.queue_name, routing_key=binding_key)
        
    def callback(self, ch, method, properties, body):
        print " [x] %r:%r" % (method.routing_key, body,)
        self._redis.sadd(self.receiver_id, body)
        #self.msgs.append(cPickle.loads(body))
        #print " [x] %r:%r" % (method.routing_key, body,)

    def process(self):
        self.channel.basic_consume(self.callback, queue=self.queue_name, no_ack=True)
        try:
            self.channel.start_consuming()
        except KeyboardInterrupt:
            self.channel.stop_consuming()
        
    def stop(self):
        self.channel.stop_consuming()
        self.connection.close()

if __name__ == '__main__':
    receiver1 = Receiver('tinglu', ['prada'])
    receiver1.process()
