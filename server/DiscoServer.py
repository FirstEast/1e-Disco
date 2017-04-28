from tornado.platform.twisted import TwistedIOLoop
from twisted.internet import reactor
from twisted.web.server import Site
from twisted.web.static import File
from autobahn.twisted.websocket import listenWS

from sockets.devices import DiscoDeviceSocketFactory, PixelPusherReceiver
from sockets.control import DiscoControlSocketFactory, DiscoControlProtocol
from sockets.inputs import BeatServerReceiverFactory, KeyInputSocketFactory, KeyInputProtocol
from model.session import DiscoSession

from pattern import *
from pattern.util import *

# Web UI config
CONTROL_WS_PORT = 9000
CONTROL_UI_PORT = 9090
CONTROL_UI_PATH = '../control_interface'

# Device network config
GOODALE_PORT = 8123
BEMIS_PORT = 8125
BEAT_PORT = 8347
KEY_PORT = 8348

if __name__ == '__main__':
  # Install the Tornado-to-Twisted bridge
  TwistedIOLoop().install()

  # Create the disco session
  session = DiscoSession()

  # Setup websocket protocol for disco commands
  factory = DiscoControlSocketFactory("ws://localhost:" + str(CONTROL_WS_PORT), session, debug = True)
  factory.protocol = DiscoControlProtocol
  listenWS(factory)

  # Setup websocket protocol for key input
  factory = KeyInputSocketFactory("ws://localhost:" + str(KEY_PORT), session, debug = True)
  factory.protocol = KeyInputProtocol
  listenWS(factory)

  # Setup socket registration for disco devices
  # TODO: Move this light reversing format stuff to the Raspis
  reactor.listenTCP(GOODALE_PORT, DiscoDeviceSocketFactory(session, "goodale", GOODALE_WIDTH, GOODALE_HEIGHT, format=GOODALE_FORMAT))
  reactor.listenTCP(BEMIS_PORT, DiscoDeviceSocketFactory(session, "bemis", BEMIS_WIDTH, BEMIS_HEIGHT, format=BEMIS_FORMAT))

  # Initialize the PixelPusherReceiver
  # ppReceiver = PixelPusherReceiver(session, "ddf", DDF_WIDTH, DDF_HEIGHT)

  # Setup socket registration for input devices
  reactor.listenTCP(BEAT_PORT, BeatServerReceiverFactory(session))

  # Setup static html serving
  resource = File(CONTROL_UI_PATH)
  staticServerFactory = Site(resource)
  reactor.listenTCP(CONTROL_UI_PORT, staticServerFactory)
  reactor.run()
