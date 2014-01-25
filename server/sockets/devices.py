from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from pattern.pattern import *

import struct

class DiscoDeviceReceiver(LineReceiver):
  def __init__(self, discoSession, name, width, height, format):
    self.discoSession = discoSession
    self.name = name
    self.width = width
    self.height = height
    self.format = format

  def sendNextFrame(self):
    output = [value for color in self.discoSession.getPattern(name).render(self).getdata() for value in color]
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
