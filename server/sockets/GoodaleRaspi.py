from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver

import cjson as json
import time

RED = [255, 0, 0]
GREEN = [0, 255, 0]
BLUE = [0, 0, 255]

class GoodaleRaspiReceiver(LineReceiver):
  def __init__(self, discoSession):
    self.discoSession = discoSession

    self.frame = 0

    self.discoSession.goodaleArduinoModel.on("change", self.updateState)

  def updateState(self, model, attr):
    self.sendMessage(self.discoSession.goodaleArduinoModel.get(attr));

  def sendNextFrame(self):
    output = [0,0,0] * 395
    output[self.frame * 3] = RED[0]
    output[self.frame * 3 + 1] = RED[1]
    output[self.frame * 3 + 2] = RED[2]
    self.sendMessage(json.encode(output).replace(" ", ""))
    
    self.frame += 1
    self.frame = self.frame % 395

  def connectionMade(self):
    self.discoSession.deviceModel.set("goodale_lounge", True)

  def connectionLost(self, reason):
    self.discoSession.deviceModel.set("goodale_lounge", False)

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