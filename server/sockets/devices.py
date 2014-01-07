from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from pattern.pattern import *

import struct

class DiscoDeviceReceiver(LineReceiver):
  def __init__(self, discoSession, deviceName, devicePattern):
    self.discoSession = discoSession
    self.deviceName = deviceName
    self.devicePattern = devicePattern

  def sendNextFrame(self):
    output = self.devicePattern.render(self)
    for i in range(0, 2):
      output = [value for sublist in output for value in sublist]
    self.sendMessage(struct.pack('B' * len(output), *output))

  def connectionMade(self):
    self.discoSession.outputDeviceModel[self.deviceName] = True

  def connectionLost(self, reason):
    self.discoSession.outputDeviceModel[self.deviceName] = False

  def dataReceived(self, line):
    if line.strip().find("OK") > -1:
      self.sendNextFrame()

  def sendMessage(self, message):
    self.transport.write(message + '\n')

class DiscoDeviceSocketFactory(Factory):
  def __init__(self, discoSession, deviceName):
    self.discoSession = discoSession
    self.deviceName = deviceName
    self.devicePattern = discoSession.patternModel[deviceName]

  def buildProtocol(self, addr):
    return DiscoDeviceReceiver(self.discoSession, self.deviceName, self.devicePattern)