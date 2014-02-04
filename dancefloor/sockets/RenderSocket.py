from twisted.internet.protocol import Protocol, ReconnectingClientFactory

import numpy
import time
import struct

from pp_herder import PPHerder

DEMO_MODULE = False

if DEMO_MODULE:
  DDF_WIDTH = 16
  DDF_HEIGHT = 12
  MODS_ACROSS = 1 #Number of modules horizontally
  NUM_MODULES = 1
else:
  DDF_WIDTH = 48
  DDF_HEIGHT = 24
  MODS_ACROSS = 3 #Number of modules horizontally
  NUM_MODULES = 6

PIX_PER_MODULE = 192
LENGTH = NUM_MODULES * PIX_PER_MODULE
MOD_WIDTH = 16 #Width of 1 module
MOD_HEIGHT = 12 #Height of 1 module
MOD_SIZE = MOD_WIDTH * MOD_HEIGHT
HALF_DDF_SIZE = MOD_SIZE * MODS_ACROSS

class RenderSocket(Protocol):
  def __init__(self):
    self.pixelpusher = False
    self.shepherd = PPHerder()
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
    output_data = numpy.reshape(new_data, (LENGTH, 3))
    for i in range(LENGTH):
      module, index = self.unSnake(i)
      self.ddf_data[module][index] = output_data[i]

  def unSnake(self, i): #i is the index of the normal array
    # returns (module id, index within module)
    mod_index = i%MOD_WIDTH
    half_ddf_index = i/HALF_DDF_SIZE
    variable = (mod_index%2*(-2)+1)*(half_ddf_index%2*(-2)+1)

    module = (i/HALF_DDF_SIZE)*MODS_ACROSS+(i%DDF_WIDTH/MOD_WIDTH)

    new_index = mod_index*MOD_HEIGHT+(variable-1)/(-2)\
      *(MOD_HEIGHT-1)+((i/DDF_WIDTH)%MOD_HEIGHT)*variable

    if module == MODS_ACROSS -1:
      new_index = MOD_HEIGHT*MOD_WIDTH - new_index - 1

    return module, new_index

  def render(self, strip):
    # print "retrieving data for strip " + str(strip)
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
