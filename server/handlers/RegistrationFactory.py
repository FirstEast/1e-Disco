from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver

class RegistrationReceiver(LineReceiver):
  def __init__(self, users):
    self.users = users
    self.name = None
    self.state = "REGISTER"

  def connectionMade(self):
    self.sendLine("Name?")

  def connectionLost(self, reason):
    if self.users.has_key(self.name):
      del self.users[self.name]

  def lineReceived(self, line):
    if self.state == "REGISTER":
      self.handle_REGISTER(line)
    else:
      self.sendLine(line)

  def handle_REGISTER(self, name):
    self.sendLine("Registered %s" % (name,))
    self.name = name
    self.users[name] = self
    self.state = "REGISTERED"


class RegistrationFactory(Factory):
  def __init__(self, users):
    self.users = users # maps user names to Chat instances

  def buildProtocol(self, addr):
    return RegistrationReceiver(self.users)