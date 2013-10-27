from autobahn.websocket import WebSocketServerProtocol, \
                                WebSocketServerFactory

class DiscoControlProtocol(WebSocketServerProtocol):
  def onMessage(self, msg, binary):
    self.factory.discoSession.trigger("message", msg)
    self.sendMessage("OK", binary)


class DiscoControlSocketFactory(WebSocketServerFactory):
  def __init__(self, url, discoSession, debug = False, debugCodePaths = False):
    WebSocketServerFactory.__init__(self, url, debug = debug, debugCodePaths = debugCodePaths)
    self.clients = []
    self.discoSession = discoSession

  def register(self, client):
    if not client in self.clients:
      self.clients.append(client)

  def unregister(self, client):
    if client in self.clients:
      self.clients.remove(client)

  def broadcast(self, msg):
    for c in self.clients:
      c.sendMessage(msg)