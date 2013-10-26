from autobahn.websocket import WebSocketServerProtocol

class DiscoProtocol(WebSocketServerProtocol):
  def onMessage(self, msg, binary):
    for name, protocol in self.getUserMap().iteritems():
      protocol.sendLine(msg)

    self.sendMessage("OK", binary)

  def getUserMap(self):
    return {}