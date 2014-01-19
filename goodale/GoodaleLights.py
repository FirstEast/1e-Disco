from twisted.internet import reactor
from twisted.internet.endpoints import TCP4ClientEndpoint
from twisted.web.server import Site
from twisted.web.static import File
from sockets.RenderSocket import *

DISCO_SERVER_HOST = "localhost"
DISCO_SERVER_PORT = 8123

if __name__ == '__main__':
  # Setup render socket
  point = TCP4ClientEndpoint(reactor, DISCO_SERVER_HOST, DISCO_SERVER_PORT)
  d = point.connect(RenderSocketFactory())
  reactor.run()