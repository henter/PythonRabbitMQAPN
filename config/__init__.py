import sys
import argparse

def get_env_config():
    parser = argparse.ArgumentParser(description='get arguments')
    parser.add_argument('-e', type=str, help='environment name')
    p = parser.parse_args()
    
    if p.e == None:
        print 'parameter error'
        sys.exit()
    
    env = p.e
    
    dev = False
    if env == 'dev':
        from config_dev import config
        dev = True
    elif env == 'test':
        from config_test import config
        dev = True
    elif env == 'prod':
        from config_prod import config
    else:
        print 'env error'
        sys.exit()
    
    config['dev'] = dev
    return config
    
def get_config():
    p = cli_parameter()
    if p.e == None or p.q == None:
        print 'parameter error'
        sys.exit()
    
    env = p.e
    
    dev = False
    if env == 'dev':
        from config_dev import config
        dev = True
    elif env == 'test':
        from config_test import config
        dev = True
    elif env == 'prod':
        from config_prod import config
    else:
        print 'env error'
        sys.exit()
    
    config['dev'] = dev
    config['queue'] = p.q
    return config

def cli_parameter():
    parser = argparse.ArgumentParser(description='get arguments')
    parser.add_argument('-q', type=str, help='queue name')
    parser.add_argument('-e', type=str, help='environment name')
    p = parser.parse_args()
    #vars = vars(parser.parse_args())

    return p
