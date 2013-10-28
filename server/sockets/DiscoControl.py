from autobahn.websocket import WebSocketServerProtocol, \
                                WebSocketServerFactory

class DiscoControlProtocol(WebSocketServerProtocol):
  def onOpen(self):
    self.factory.register(self)
    # TODO: send initial state message

  def onMessage(self, msg, binary):
    self.factory.discoSession.goodaleArduinoModel.set("state", msg);
    self.sendMessage("OK", binary)

  def connectionLost(self, reason):
    WebSocketServerProtocol.connectionLost(self, reason)
    self.factory.unregister(self)


class DiscoControlSocketFactory(WebSocketServerFactory):
  def __init__(self, url, discoSession, debug = False, debugCodePaths = False):
    WebSocketServerFactory.__init__(self, url, debug = debug, debugCodePaths = debugCodePaths)
    self.clients = []
    self.discoSession = discoSession

    self.discoSession.deviceModel.on("change", self.deviceChange)

  def deviceChange(self, model, attr):
    self.broadcast(attr + ": " + str(model.get(attr)))

  def register(self, client):
    if not client in self.clients:
      self.clients.append(client)

  def unregister(self, client):
    if client in self.clients:
      self.clients.remove(client)

  def broadcast(self, msg):
    for c in self.clients:
      c.sendMessage(msg)