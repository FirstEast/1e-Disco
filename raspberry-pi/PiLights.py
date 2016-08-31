from twisted.internet import reactor
from twisted.internet.endpoints import TCP4ClientEndpoint
from twisted.web.server import Site
from twisted.web.static import File
from sockets.RenderSocket import *

import os

USB_PREFIX = '/media/'

if __name__ == '__main__':
  # Sleep while Raspi wakes up (hack)
  time.sleep(10)

  usb = os.walk(USB_PREFIX).next()[1][0]
  # Use auto ssh?
  config = USB_PREFIX + usb + '/config.txt'
  host = ''
  port = 0
  length = 0
  with open(config, 'r') as f:
    host = f.readline().strip()
    port = int(f.readline().strip())
    length = int(f.readline().strip())

  print host
  print port
  print length

  # Setup render socket
  point = TCP4ClientEndpoint(reactor, host, port)
  d = point.connect(RenderSocketFactory(length))
  reactor.run()
