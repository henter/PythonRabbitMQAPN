import socket, ssl, json, struct
import binascii

def Payload(alert='', badge=1, data={}):
     payload = {
        'aps': {
            'alert':alert,
            'sound':'k1DiveAlarm.caf',
            'badge':badge,
         },
        'acme': data,
     }
     return payload


class APN(object):
    def __init__(self, cert_file=None, dev=False):
        super(APN, self).__init__()
        self.cert_file = cert_file
        self.dev = dev
        self.connection = None
        
    def get_connection(self):
        if not self.connection:
            self.connection = APNConnection(cert_file = self.cert_file, dev = self.dev)
        return self.connection
        

    def send(self, token=None, payload=None):
        
        data = json.dumps( payload , ensure_ascii=False)
        #data = json.dumps( payload )
        data = data.encode('utf-8')

        # Clear out spaces in the device token and convert to hex
        deviceToken = token.replace(' ','')
        byteToken = binascii.unhexlify(token)
        theFormat = '!BH32sH%ds' % len(data)
        theNotification = struct.pack( theFormat, 0, 32, byteToken, len(data), data )


        retry_time_limit = 3
        isFail = True
        tryTime = 0
        while isFail and tryTime < retry_time_limit:
            try:
                ret = self.get_connection().write(theNotification)
                isFail = False
            except :
                isFail = True
                tryTime += 1
                print("apn try " + str(tryTime) + " time failed, time out.")
                
        if isFail:
            return False
            
        return True if int(ret)<=293 else False


class APNConnection(object):

    def __init__(self, cert_file=None, dev=False):
        super(APNConnection, self).__init__()
        self.cert_file = cert_file
        self.ssl_sock = None
        self.server = 'gateway.push.apple.com'
        if dev == True:
            self.server = 'gateway.sandbox.push.apple.com'

        self.port = 2195

    def connect(self):
        self.ssl_sock = ssl.wrap_socket(
                socket.socket( socket.AF_INET, socket.SOCK_STREAM ),
                certfile = self.cert_file
            )
        self.ssl_sock.connect( (self.server, self.port) )
        return self.ssl_sock

    def get_connection(self):
        if not self.ssl_sock:
            self.connect()
        return self.ssl_sock

    def read(self, n=None):
        return self.get_connection().read(n)

    def write(self, string):
        return self.get_connection().write(string)

    def __del__(self):
        if self.ssl_sock:
            self.ssl_sock.close()
