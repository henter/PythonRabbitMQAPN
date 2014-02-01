#coding=utf-8
import threading

class thread_manager:
    def __init__(self, thread_num=1, target=None):
        print 'start thread manager ...'
        for i in range(thread_num):
            th = threading.Thread(target=target, args=(i,))
            th.setDaemon(True)
            th.start()
