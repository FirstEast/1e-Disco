from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver

class GoodaleArduinoReceiver(LineReceiver):
  def __init__(self, discoSession):
    self.discoSession = discoSession
    self.ready = False

    # TODO: bind listeners to goodale arduino light model changes

  def connectionMade(self):
    self.discoSession.deviceModel.set("goodale_arduino", True)

  def connectionLost(self, reason):
    self.discoSession.deviceModel.set("goodale_arduino", False)

  def lineReceived(self, line):
    # TODO: update ready state to True based on line
    pass

  def sendMessage(self, model, message):
    self.transport.write(message + '\n')


class GoodaleArduinoSocketFactory(Factory):
  def __init__(self, discoSession):
    self.discoSession = discoSession # maps user names to Chat instances

  def buildProtocol(self, addr):
    return GoodaleArduinoReceiver(self.discoSession)