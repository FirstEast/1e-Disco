from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver

import cPickle as pickle
import json
import time

RED = [255, 0, 0]
BLUE = [0, 0, 255]

class GoodaleRaspiReceiver(LineReceiver):
  def __init__(self, discoSession):
    self.discoSession = discoSession

    self.color = RED

    self.discoSession.goodaleArduinoModel.on("change", self.updateState)

  def updateState(self, model, attr):
    self.sendMessage(self.discoSession.goodaleArduinoModel.get(attr));

  def sendNextFrame(self):
    self.sendMessage(json.dumps(self.color * 1185).replace(" ", ""))
    if self.color == RED:
      self.color = BLUE
    else:
      self.color = RED

  def connectionMade(self):
    self.discoSession.deviceModel.set("goodale_arduino", True)

  def connectionLost(self, reason):
    self.discoSession.deviceModel.set("goodale_arduino", False)

  def dataReceived(self, line):
    if line.strip().find("OK") > -1:
      time.sleep(0.04)
      self.sendNextFrame()

  def sendMessage(self, message):
    self.transport.write(message + '\n')


class GoodaleRaspiSocketFactory(Factory):
  def __init__(self, discoSession):
    self.discoSession = discoSession

  def buildProtocol(self, addr):
    return GoodaleRaspiReceiver(self.discoSession)