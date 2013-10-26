from twisted.internet import reactor
from twisted.web.server import Site
from twisted.web.static import File

from autobahn.websocket import WebSocketServerFactory, listenWS

from handlers.RegistrationFactory import *
from handlers.DiscoProtocol import *

if __name__ == '__main__':
  # TODO: This protocol class creation and factory instantiation
  # should be in a meta class
  userMap = {}

  # Dynamically generated subclass, to get the same userMap in the protocols
  class MappedDiscoProtocol(DiscoProtocol):
    def getUserMap(self):
      return userMap

  # Setup websocket protocol for disco commands
  factory = WebSocketServerFactory("ws://localhost:9000", debug = False)
  factory.protocol = MappedDiscoProtocol
  listenWS(factory)

  # Setup socket registration for disco devices
  reactor.listenTCP(8123, RegistrationFactory(userMap))

  # Setup static html serving
  resource = File('../interface')
  staticServerFactory = Site(resource)
  reactor.listenTCP(80, staticServerFactory)
  reactor.run()