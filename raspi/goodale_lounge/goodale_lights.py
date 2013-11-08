from twisted.internet import reactor
from twisted.internet.endpoints import TCP4ClientEndpoint
from twisted.web.server import Site
from twisted.web.static import File

from autobahn.websocket import listenWS

from sockets.RenderSocket import *
from sockets.VisualizeWebSocket import *

DISCO_SERVER_HOST = "localhost"
DISCO_SERVER_PORT = 8123

WEB_SOCKET_PORT = 1111

INTERFACE_DIR = "interface"
INTERFACE_PORT = 90

if __name__ == '__main__':
  # Setup web visual socket
  visualizeFactory = VisualizeWebSocketFactory("ws://localhost:" + str(WEB_SOCKET_PORT), debug = False)
  visualizeFactory.protocol = VisualizeWebSocket
  listenWS(visualizeFactory)

  # Setup render socket
  point = TCP4ClientEndpoint(reactor, DISCO_SERVER_HOST, DISCO_SERVER_PORT)
  d = point.connect(RenderSocketFactory(visualizeFactory))

  # Setup static html serving
  resource = File(INTERFACE_DIR)
  staticServerFactory = Site(resource)
  reactor.listenTCP(INTERFACE_PORT, staticServerFactory)
  reactor.run()

# red = [255, 0, 0]
# blue = [0, 0, 255] 

# # These might be changed if we expand
# num_leds = 396
# pixel_size = 3

# # For WS2801
# gamma = bytearray(256)
# for i in range(256):
#     gamma[i] = int(pow(float(i) / 255.0, 2.5) * 255.0)

# output = bytearray(num_leds * pixel_size + 3)

# def filter_pixel(input_pixel, brightness):
#     input_pixel[0] = brightness * input_pixel[0]
#     input_pixel[1] = brightness * input_pixel[1]
#     input_pixel[2] = brightness * input_pixel[2]

#     output_pixel = bytearray(pixel_size)
#     output_pixel[0] = gamma[input_pixel[0]]
#     output_pixel[1] = gamma[input_pixel[1]]
#     output_pixel[2] = gamma[input_pixel[2]]
#     return output_pixel

# color = red
# while True:
#     for led in range(num_leds):
#         output[led * pixel_size:] = filter_pixel(color, 1)
#     if color == red:
#         color = blue
#     else:
#         color = red
#     spidev.write(output)
#     spidev.flush()
#     time.sleep(0.1)

