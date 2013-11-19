from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver

import json

class BeatServerReceiver(LineReceiver):
  def __init__(self, discoSession):
    self.discoSession = discoSession
    self.beatModel = self.discoSession.beatModel

  def connectionMade(self):
    self.discoSession.deviceModel["beat"] = True
    self.sendMessage("OK")

  def connectionLost(self, reason):
    self.discoSession.deviceModel["beat"] = False

  def dataReceived(self, line):
    data = json.loads(line.strip())
    self.beatModel.updateData(data['leftCentroid'], data['leftVolume'], data['leftFrequencies'],\
                              data['rightCentroid'], data['rightVolume'], data['rightFrequencies'])
    self.sendMessage("OK")

  def sendMessage(self, message):
    self.transport.write(message + '\n')

class BeatServerReceiverFactory(Factory):
  def __init__(self, discoSession):
    self.discoSession = discoSession

  def buildProtocol(self, addr):
    return BeatServerReceiver(self.discoSession)