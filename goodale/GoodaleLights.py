from twisted.internet import reactor
from twisted.internet.endpoints import TCP4ClientEndpoint
from twisted.web.server import Site
from twisted.web.static import File

from autobahn.twisted.websocket import listenWS

from sockets.RenderSocket import *
from sockets.VisualizeWebSocket import *

DISCO_SERVER_HOST = "localhost"
DISCO_SERVER_PORT = 8123

WEB_SOCKET_PORT = 1111

if __name__ == '__main__':
  # Setup web visual socket
  visualizeFactory = VisualizeWebSocketFactory("ws://localhost:" + str(WEB_SOCKET_PORT), debug = False)
  visualizeFactory.protocol = VisualizeWebSocket
  listenWS(visualizeFactory)

  # Setup render socket
  point = TCP4ClientEndpoint(reactor, DISCO_SERVER_HOST, DISCO_SERVER_PORT)
  d = point.connect(RenderSocketFactory(visualizeFactory))
  reactor.run()