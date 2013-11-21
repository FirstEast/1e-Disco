from twisted.internet import reactor
from twisted.web.server import Site
from twisted.web.static import File
from autobahn.websocket import listenWS

from sockets.devices import DiscoDeviceSocketFactory
from sockets.control import DiscoControlSocketFactory, DiscoControlProtocol
from sockets.inputs import BeatServerReceiverFactory
from model.session import DiscoSession

from pattern import *

if __name__ == '__main__':
  # Create the disco session
  session = DiscoSession()

  # Setup websocket protocol for disco commands
  factory = DiscoControlSocketFactory("ws://localhost:9000", session, debug = False)
  factory.protocol = DiscoControlProtocol
  listenWS(factory)

  # Setup socket registration for disco devices
  reactor.listenTCP(8123, DiscoDeviceSocketFactory(session, "goodale", session.goodalePattern, 1))
  reactor.listenTCP(8124, DiscoDeviceSocketFactory(session, "ddf", session.ddfPattern, 2))

  # Setup socket registration for input devices
  reactor.listenTCP(8347, BeatServerReceiverFactory(session))

  # Setup static html serving
  resource = File('../control_interface')
  staticServerFactory = Site(resource)
  reactor.listenTCP(80, staticServerFactory)
  reactor.run()