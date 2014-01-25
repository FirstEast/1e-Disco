from twisted.internet.protocol import Protocol, ReconnectingClientFactory

import numpy
import time
import struct

from pp_herder import PPHerder

# WIDTH = 48
# HEIGHT = 24
NUM_MODULES = 6
PIX_PER_MODULE = 192
LENGTH = NUM_MODULES * PIX_PER_MODULE
# DDF_ARRAY = numpy.arange(LENGTH*3).reshape(NUM_MODULES, PIX_PER_MODULE, 3)
# DDF_INDEX = {key: tuple(value) for key in range(LENGTH*3) for value in numpy.argwhere(DDF_ARRAY==key)}

class RenderSocket(Protocol):
  def __init__(self):
    self.pixelpusher = False
    self.shepherd = PPHerder()
    # self.ddf_data = numpy.zeros(LENGTH*3).reshape(NUM_MODULES, PIX_PER_MODULE, 3)
    # ddf_data variable is a dictionary, where the key is the module number ("strip"
    # number on pixelpusher), and the value is the data for that module.
    self.ddf_data = {key: numpy.zeros(PIX_PER_MODULE*3).reshape(PIX_PER_MODULE, 3) for key in range(6)}

    callback = lambda device: device.start_updates_with_source(self.render)
    self.shepherd.add_callbacks(found=callback)

    def on_connect(device):
      self.pixelpusher = True
      print ("Found PixelPusher at Mac Address %s  - "
      "IP Address  %s" % (device.packet.header.mac_str(), device.packet.header.ip_str()))

    def on_lost(device):
      self.pixelpusher = False
      self.shepherd.remove_callback(callback)
      print "PixelPusher connection lost: %s" % device.packet.header.ip_str()

    self.shepherd.add_callbacks(found=on_connect, lost=on_lost)

  def connectionMade(self):
    print "connected successfully to central server"
    time.sleep(1)

    # Signal for the next frame
    self.sendMessage("OK")

  def dataReceived(self, line):
    # Parse what we got to the int array
    line = line.strip()
    output = []
    try:
      output = struct.unpack('B'*LENGTH*3, line)
    except struct.error:
      # print "Struct Error"
      self.sendMessage("OK")
      return

    # If we're running on a pixelpusher, render the stuff we got,
    # otherwise send it to the web visualizer as json
    if self.pixelpusher:
      self.update(output)

    # Signal for the next frame
    self.sendMessage("OK")

  def update(self, new_data):
    ddf_output = self.ddfConversion(new_data)
    self.ddf_data = ddf_output

  # Yes, I know this is really dumb and inefficient. It's 5 AM. I'm sorry.
  def ddfConversion(self, data):
    ddf_output = self.ddf_data
    for i in range(LENGTH):
      # index = DDF_INDEX[i]
      module, index = self.unSnake(i)
      output_data = numpy.reshape(data, (LENGTH, 3))
      ddf_output[module][index] = output_data[i]
    return ddf_output

  def unSnake(self, i): #i is the index of the normal array
    Wm=16 #Width of 1 module
    Hm=12 #Height of 1 module
    W=3 #Nb of modules horizontally
    #(module id, index within module)
    module = (i/(Hm*Wm*W))*W+(i%(Wm*W)/Wm)
    new_index = (i%Wm)*Hm+((((i%Wm)%2)*(-2)+1)*(((i/(Wm*Hm*W))%2)\
      *(-2)+1)-1)/(-2)*(Hm-1)+(((i/(W*Wm))%Hm))*(((i%Wm)%2)*(-2)+1)*(((i/(Wm*Hm*W))%2)*(-2)+1)
    if module > 5:
      print i
    return module, new_index

  def render(self, strip):
    # print "retrieving data for strip " + str(strip)
    # # scale = lambda data: int(0x55 * (data+1) / 2)
    # scale = lambda data: int(data)
    try:
      module_data = self.ddf_data[strip]
      intlist = map(int, module_data.flatten().tolist())
      return intlist
    except IndexError:
      print "IndexError"
      return [0,0,0] * PIX_PER_MODULE

  def sendMessage(self, message):
    self.transport.write(message + '\n')

class RenderSocketFactory(ReconnectingClientFactory):
  def buildProtocol(self, addr):
    self.resetDelay()
    return RenderSocket()

  def clientConnectionLost(self, connector, reason):
    ReconnectingClientFactory.clientConnectionLost(self, connector, reason)

  def clientConnectionFailed(self, connector, reason):
    ReconnectingClientFactory.clientConnectionFailed(self, connector,
                                                     reason)
