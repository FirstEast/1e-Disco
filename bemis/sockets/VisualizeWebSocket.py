from autobahn.websocket import WebSocketServerProtocol, \
                                WebSocketServerFactory

class VisualizeWebSocket(WebSocketServerProtocol):
  def onOpen(self):
    self.factory.register(self)

  def connectionLost(self, reason):
    WebSocketServerProtocol.connectionLost(self, reason)
    self.factory.unregister(self)

class VisualizeWebSocketFactory(WebSocketServerFactory):
  def __init__(self, url, debug = False, debugCodePaths = False):
    WebSocketServerFactory.__init__(self, url, debug = debug, debugCodePaths = debugCodePaths)
    self.clients = []

  def register(self, client):
    if not client in self.clients:
      self.clients.append(client)

  def unregister(self, client):
    if client in self.clients:
      self.clients.remove(client)

  def broadcast(self, msg):
    for c in self.clients:
      c.sendMessage(msg)