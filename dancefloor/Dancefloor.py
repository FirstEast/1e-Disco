from tornado.platform.twisted import TwistedIOLoop
from twisted.internet import reactor
from twisted.internet.endpoints import TCP4ClientEndpoint
from twisted.web.server import Site
from twisted.web.static import File
from sockets.RenderSocket import *

DISCO_SERVER_HOST = "localhost"
DISCO_SERVER_PORT = 8124

if __name__ == '__main__':
  # Install the Tornado-to-Twisted bridge
  TwistedIOLoop().install()

  # Setup render socket
  point = TCP4ClientEndpoint(reactor, DISCO_SERVER_HOST, DISCO_SERVER_PORT)
  d = point.connect(RenderSocketFactory())
  reactor.run()
