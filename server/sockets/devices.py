from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from pattern.pattern import *
from pattern.util import *
from sockets.control import *
from pixelpusher.pp_herder import PPHerder

import struct, numpy

DEMO_MODULE = False

if DEMO_MODULE:
  DDF_WIDTH = 16
  DDF_HEIGHT = 12
  MODS_ACROSS = 1 # Number of modules horizontally
  NUM_MODULES = 1
else:
  DDF_WIDTH = 48
  DDF_HEIGHT = 24
  MODS_ACROSS = 3 # Number of modules horizontally
  NUM_MODULES = 6

PIX_PER_MODULE = 192
LENGTH = NUM_MODULES * PIX_PER_MODULE
MOD_WIDTH = 16    # Width of 1 module
MOD_HEIGHT = 12   # Height of 1 module
MOD_SIZE = MOD_WIDTH * MOD_HEIGHT
HALF_DDF_SIZE = MOD_SIZE * MODS_ACROSS

class DiscoDeviceReceiver(LineReceiver):
  def __init__(self, discoSession, name, width, height, format):
    self.discoSession = discoSession
    self.name = name
    self.width = width
    self.height = height
    self.format = format

  def sendNextFrame(self):
    if self.name == 'goodale' and self.discoSession.getPattern(self.name).__class__.__name__ == 'MimicPattern':
      frame = unflattenGoodaleArray(flatGoodaleArrayFromDdfImage(self.discoSession.getPattern('ddf').render(MOCK_DEVICES['ddf']))).getdata()
    else:
      frame = self.discoSession.getPattern(self.name).render(self).getdata()

    if self.format == 'BGR':
      newFrame = []
      for color in frame:
        newFrame.append((color[2], color[1], color[0]))
      frame = newFrame

    output = [value for color in frame for value in color]
    self.sendMessage(struct.pack('B' * len(output), *output))

  def connectionMade(self):
    self.discoSession.outputDeviceModel[self.name] = True

  def connectionLost(self, reason):
    self.discoSession.outputDeviceModel[self.name] = False

  def dataReceived(self, line):
    if line.strip().find("OK") > -1:
      self.sendNextFrame()

  def sendMessage(self, message):
    self.transport.write(message + '\n')

class DiscoDeviceSocketFactory(Factory):
  def __init__(self, discoSession, name, width, height, format='RGB'):
    self.discoSession = discoSession
    self.name = name
    self.width = width
    self.height = height
    self.format = format

  def buildProtocol(self, addr):
    return DiscoDeviceReceiver(self.discoSession, self.name, self.width, self.height, self.format)


class PixelPusherReceiver():
  def __init__(self, discoSession, name, width, height, format='RGB'):
    self.discoSession = discoSession
    self.name = name
    self.width = width
    self.height = height
    self.format = format

    self.pixelpusher = False
    self.shepherd = PPHerder()
    # ddf_data variable is a dictionary, where the key is the module number ("strip"
    # number on pixelpusher), and the value is the data for that module.
    self.ddf_data = {key: numpy.zeros(PIX_PER_MODULE*3).reshape(PIX_PER_MODULE, 3) for key in range(6)}

    callback = lambda device: device.start_updates_with_source(self.render)
    self.shepherd.add_callbacks(found=callback)

    def on_connect(device):
      self.pixelpusher = True
      self.discoSession.outputDeviceModel[self.name] = True
      print ("Found PixelPusher at Mac Address %s  - "
      "IP Address  %s" % (device.packet.header.mac_str(), device.packet.header.ip_str()))

    def on_lost(device):
      self.pixelpusher = False
      self.discoSession.outputDeviceModel[self.name] = False
      self.shepherd.remove_callback(callback)
      print "PixelPusher connection lost: %s" % device.packet.header.ip_str()

    self.shepherd.add_callbacks(found=on_connect, lost=on_lost)

  def renderNewFrame(self):
    frame = self.discoSession.getPattern(self.name).render(self).getdata()
    new_data = [value for color in frame for value in color]
    output_data = numpy.reshape(new_data, (LENGTH, 3))
    for i in range(LENGTH):
      module, index = self.unSnake(i)
      self.ddf_data[module][index] = output_data[i]

  def unSnake(self, i):
    #i is the index of the normal array
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
    if strip == 1:
      self.renderNewFrame()

    try:
      module_data = self.ddf_data[strip]
      intlist = map(int, module_data.flatten().tolist())
      return intlist
    except IndexError:
      print "IndexError"
      return [0,0,0] * PIX_PER_MODULE
