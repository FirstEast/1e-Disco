from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver

class GoodaleRaspiReceiver(LineReceiver):
  def __init__(self, discoSession):
    self.discoSession = discoSession
    self.ready = False

    self.discoSession.goodaleArduinoModel.on("change", self.updateState)

  def updateState(self, model, attr):
    self.sendMessage(self.discoSession.goodaleArduinoModel.get(attr));

  def connectionMade(self):
    self.discoSession.deviceModel.set("goodale_arduino", True)

  def connectionLost(self, reason):
    self.discoSession.deviceModel.set("goodale_arduino", False)

  def lineReceived(self, line):
    # TODO: update ready state to True based on line
    pass

  def sendMessage(self, message):
    self.transport.write(message + '\n')


class GoodaleRaspiSocketFactory(Factory):
  def __init__(self, discoSession):
    self.discoSession = discoSession

  def buildProtocol(self, addr):
    return GoodaleRaspiReceiver(self.discoSession)