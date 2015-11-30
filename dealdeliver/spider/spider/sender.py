'''
Created on Sep 7, 2015

@author: xuyan_000
'''

import cPickle
import pika
import sys
import time

#kafkaS = KafkaClient('localhost:9092')
#producer = SimpleProducer(kafkaS)
#topic = 't o p%i/c'
#msg_str_dict = {'ascd':123}
#producer.send_messages(topic_fill(topic), cPickle.dumps(msg_str_dict))


def topic_fill(top_str):
    new_str = ''
    for c in top_str:
        if (c >= 'a' and c <= 'z') or (c >= 'A' and c <= 'Z'):
            new_str += c.lower()
    return new_str

        
class Sender(object):
    
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange='topic_news', type='topic')
    
    def send_message(self, routing_key, message):
        #routing_key = '#.' + topic_fill(routing_key) + '.#'
        routing_key = topic_fill(routing_key)
        self.channel.basic_publish(exchange='topic_news', routing_key=routing_key, body=cPickle.dumps(message))
    
    def stop(self):
        self.connection.close()

if __name__ == '__main__':
    sender = Sender()
    sender.send_message('a b c', 'how are you from a')
    sender.send_message('a%b/c', 'how are you from b')
    sender.send_message('de', 'how are you from c')
    #sender.stop()
