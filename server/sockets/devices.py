from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from pattern.Pattern import *

import struct

class GoodaleRaspiReceiver(LineReceiver):
  def __init__(self, discoSession):
    self.discoSession = discoSession

  def sendNextFrame(self):
    output = self.discoSession.goodalePattern.getNextFrame()
    self.sendMessage(struct.pack('B' * Pattern.GOODALE_WIDTH * 3, *output))

  def connectionMade(self):
    self.discoSession.deviceModel.set("goodale", True)

  def connectionLost(self, reason):
    self.discoSession.deviceModel.set("goodale", False)

  def dataReceived(self, line):
    if line.strip().find("OK") > -1:
      self.sendNextFrame()

  def sendMessage(self, message):
    self.transport.write(message + '\n')

class GoodaleRaspiSocketFactory(Factory):
  def __init__(self, discoSession):
    self.discoSession = discoSession

  def buildProtocol(self, addr):
    return GoodaleRaspiReceiver(self.discoSession)


class DDFPixelPusherReceiver(LineReceiver):
  def __init__(self, discoSession):
    self.discoSession = discoSession

  def sendNextFrame(self):
    frame = self.discoSession.ddfPattern.getNextFrame()
    output = [item for sublist in frame for color in sublist for item in color]
    self.sendMessage(struct.pack('B' * Pattern.DDF_WIDTH * Pattern.DDF_HEIGHT * 3, *output))

  def connectionMade(self):
    self.discoSession.deviceModel.set("ddf", True)

  def connectionLost(self, reason):
    self.discoSession.deviceModel.set("ddf", False)

  def dataReceived(self, line):
    if line.strip().find("OK") > -1:
      self.sendNextFrame()

  def sendMessage(self, message):
    self.transport.write(message + '\n')

class DDFPixelPusherSocketFactory(Factory):
  def __init__(self, discoSession):
    self.discoSession = discoSession

  def buildProtocol(self, addr):
    return DDFPixelPusherReceiver(self.discoSession)