from twisted.internet import reactor
from twisted.web.server import Site
from twisted.web.static import File
from autobahn.twisted.websocket import listenWS

from sockets.devices import DiscoDeviceSocketFactory
from sockets.control import DiscoControlSocketFactory, DiscoControlProtocol
from sockets.inputs import BeatServerReceiverFactory
from model.session import DiscoSession

from pattern import *
from pattern.util import *

# Web UI config
CONTROL_WS_PORT = 9000
CONTROL_UI_PORT = 80
CONTROL_UI_PATH = '../control_interface'

# Device network config
GOODALE_PORT = 8123
DDF_PORT = 8124
BEMIS_PORT = 8125
BEAT_PORT = 8347

if __name__ == '__main__':
  # Create the disco session
  session = DiscoSession()

  # Setup websocket protocol for disco commands
  factory = DiscoControlSocketFactory("ws://localhost:" + str(CONTROL_WS_PORT), session, debug = True)
  factory.protocol = DiscoControlProtocol
  listenWS(factory)

  # Setup socket registration for disco devices
  reactor.listenTCP(GOODALE_PORT, DiscoDeviceSocketFactory(session, "goodale", GOODALE_WIDTH, GOODALE_HEIGHT, format=GOODALE_FORMAT))
  reactor.listenTCP(DDF_PORT, DiscoDeviceSocketFactory(session, "ddf", DDF_WIDTH, DDF_HEIGHT))
  reactor.listenTCP(BEMIS_PORT, DiscoDeviceSocketFactory(session, "bemis", BEMIS_WIDTH, BEMIS_HEIGHT))

  # Setup socket registration for input devices
  reactor.listenTCP(BEAT_PORT, BeatServerReceiverFactory(session))

  # Setup static html serving
  resource = File(CONTROL_UI_PATH)
  staticServerFactory = Site(resource)
  reactor.listenTCP(CONTROL_UI_PORT, staticServerFactory)
  reactor.run()
