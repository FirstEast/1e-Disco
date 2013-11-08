from twisted.internet import reactor
from twisted.web.server import Site
from twisted.web.static import File

from autobahn.websocket import listenWS

from sockets.GoodaleRaspi import *
from sockets.DiscoControl import *

from model.DiscoSession import *

if __name__ == '__main__':
  # Create the disco session
  session = DiscoSession()

  # Setup websocket protocol for disco commands
  factory = DiscoControlSocketFactory("ws://localhost:9000", session, debug = False)
  factory.protocol = DiscoControlProtocol
  listenWS(factory)

  # Setup socket registration for disco devices
  reactor.listenTCP(8123, GoodaleRaspiSocketFactory(session))

  # Setup static html serving
  resource = File('../control_interface')
  staticServerFactory = Site(resource)
  reactor.listenTCP(80, staticServerFactory)
  reactor.run()