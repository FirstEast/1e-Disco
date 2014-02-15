from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from pattern.util import BEAT_MODEL

import json

class BeatServerReceiver(LineReceiver):
  def __init__(self, discoSession):
    self.discoSession = discoSession
    self.beatModel = BEAT_MODEL

  def connectionMade(self):
    self.discoSession.inputDeviceModel["beat"] = True
    self.sendMessage("OK")

  def connectionLost(self, reason):
    self.discoSession.inputDeviceModel["beat"] = False

  def dataReceived(self, line):
    data = json.loads(line.strip())
    self.beatModel.updateData(data['centroid'], data['volume'], data['frequencies'])
    self.sendMessage("OK")

  def sendMessage(self, message):
    self.transport.write(message + '\n')

class BeatServerReceiverFactory(Factory):
  def __init__(self, discoSession):
    self.discoSession = discoSession

  def buildProtocol(self, addr):
    return BeatServerReceiver(self.discoSession)