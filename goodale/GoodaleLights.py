from twisted.internet import reactor
from twisted.internet.endpoints import TCP4ClientEndpoint
from twisted.web.server import Site
from twisted.web.static import File
from sockets.RenderSocket import *

import os

USB_PREFIX = '/media/'

DISCO_SERVER_HOST = "localhost"
DISCO_SERVER_PORT = 8123

if __name__ == '__main__':
  usb = os.walk(USB_PREFIX).next()[1][0]
  config = USB_PREFIX + usb + '/config.txt'
  host = ''
  with open(config, 'r') as f:
    host = f.readline()
  
  # Setup render socket
  point = TCP4ClientEndpoint(reactor, host, DISCO_SERVER_PORT)
  d = point.connect(RenderSocketFactory())
  reactor.run()
