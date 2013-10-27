from twisted.internet import reactor
from twisted.web.server import Site
from twisted.web.static import File

from autobahn.websocket import WebSocketServerFactory, listenWS

from sockets.GoodaleArduino import *
from sockets.DiscoControl import *

from model.Model import *

if __name__ == '__main__':
  testModel = Model({})

  # Setup websocket protocol for disco commands
  factory = DiscoControlSocketFactory("ws://localhost:9000", testModel, debug = False)
  factory.protocol = DiscoControlProtocol
  listenWS(factory)

  # Setup socket registration for disco devices
  reactor.listenTCP(8123, GoodaleArduinoSocketFactory(testModel))

  # Setup static html serving
  resource = File('../interface')
  staticServerFactory = Site(resource)
  reactor.listenTCP(80, staticServerFactory)
  reactor.run()