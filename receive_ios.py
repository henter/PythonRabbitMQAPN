#!/usr/bin/env python
#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import threading
import time
import pika
import json
from thread_manager import thread_manager

from config import get_config
from push_ios import push

def main(thread_id):
    thread_str = 'Thread %s : ' % str(thread_id)
    
    user = config['user']
    password = config['password']
    queue = config['queue']

    queue_size = get_queue_size()
    
    try:
        credentials = pika.PlainCredentials(user, password)
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost',5672,'/',credentials))

        channel = connection.channel()
        channel.queue_declare(queue=queue,durable=True)
    except:
        print 'rabbitmq conneciton fail'
        sys.exit()
        
    print thread_str + ' [*] Waiting for messages. To exit press CTRL+C'
    
    def callback(ch, method, properties, body):
        #print " [x] Received json "+ (body)
        print thread_str + " [x] Received... "
        ret = push(json.loads(body), config)
        if ret == True:
            print thread_str + "push success "+ body
        else:
            print thread_str + 'push fail: '+body
        ch.basic_ack(delivery_tag = method.delivery_tag)
        ch.stop_consuming()

    channel.basic_qos(prefetch_count=10)
    channel.basic_consume(callback, queue=queue)
    
    if queue_size > 0:
        #print thread_str + 'start consuming...'
        #这里如果开启consuming会阻塞
        #channel.start_consuming()
        pass
    else:
        print thread_str + 'queue is empty, stop consuming'
        channel.stop_consuming()
    connection.close()

def get_queue_size():
    user = config['user']
    password = config['password']
    queue = config['queue']
    
    try:
        credentials = pika.PlainCredentials(user, password)
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost',5672,'/',credentials))

        channel = connection.channel()
        declare_ok = channel.queue_declare(queue=queue,durable=True,passive=True)
        return declare_ok.method.message_count
    except:
        print 'rabbitmq conneciton fail while get queue size'
        return 0
    
def get_thread_num(queue_size):
    global _sleep
    if queue_size > 100:
        thread_num = 100
        _sleep = 0.1
    elif queue_size > 10:
        thread_num = 5
        _sleep = 0.1
    else:
        thread_num = 2
        _sleep = 2
    return thread_num


if __name__ == '__main__':
    config = get_config()
    if not config:
        print 'config error'
        sys.exit()
    
    _sleep = 2
    thread_num = get_thread_num(get_queue_size())
    
    # 防止KeyboardInterrupt时报错，程序会在下一步捕获KeyboardInterrupt
    try:
        thread_manager(thread_num, main)
    except:
        pass
        
    
    # 所有线程执行完退出后 循环检查
    try:
        while True:
            time.sleep(_sleep)
            print 'all threads exit. loop checking...'
            
            queue_size = get_queue_size();
            if queue_size > 0:
                thread_manager(get_thread_num(queue_size), main)
    except KeyboardInterrupt:
        print "\nthread manager stoped"