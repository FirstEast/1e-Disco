from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver

class GoodaleArduinoReceiver(LineReceiver):
  def __init__(self, discoSession):
    self.discoSession = discoSession
    self.ready = False

    self.discoSession.on("message", self.sendMessage)

    # TODO: bind listeners to goodale arduino light model changes

  def connectionMade(self):
    # TODO: update session with goodale arduino connection
    pass

  def connectionLost(self, reason):
    # TODO: update session with lost goodale arduino connection
    pass

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