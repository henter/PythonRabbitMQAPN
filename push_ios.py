#!/usr/bin/env python
#coding=utf-8
import sys
from api.apns import APN,Payload

#msg : {'udid':'fdsagdsafsdfs','app':'test','content':'xxx', 'count':1, 'data':{}}
def push(msg, config):
    token = msg['udid']
    data = msg['data']
    if len(token) < 50:
        return 'udid invalid'

    payload = Payload(msg['content'], msg['count'], data)
    
    #不同的app用不同证书
    if 'app' in msg:
        pem = config[msg['app']]['pem']
    else:
        return 'app error'
    
    apn = APN(pem, config['dev'])
    return apn.send(token, payload)

if __name__ == '__main__':
    from config import get_env_config

    msg = {
        'app': 'test',
        'data': {'type':'feed', 'id': 123},
        'count': 1,
        'udid': 'bf7124b455c46395d619046df2b1fe68aed9cb8c2dd6b5a9f8531exxxxxxxxxx',
        'content':u'44445萨范德萨范德萨范德萨范德萨范德萨范德萨范德萨范德萨范德萨范德萨范德萨范德萨范德萨范德萨范德萨范德'
    }

    config = get_env_config()
    if not config:
        print 'config error'

    print push(msg, config)
