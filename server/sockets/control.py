from autobahn.websocket import WebSocketServerProtocol, \
                                WebSocketServerFactory

from pattern.importer import *

class DiscoControlProtocol(WebSocketServerProtocol):
  def onOpen(self):
    self.factory.register(self)
    self.sendMessage(getPatternMapJson())

    # Starting mock patterns, to demo in the viewer prior to swaps
    # Need one set per client
    self.mockPatternModel = self.factory.discoSession.patternModel

  def onMessage(self, msg, binary):
    # TODO: control protocols!
    self.sendMessage("OK", binary)

  def connectionLost(self, reason):
    WebSocketServerProtocol.connectionLost(self, reason)
    self.factory.unregister(self)

  def performSwap(self, deviceName):
    self.factory.discoSession.patternModel[deviceName] = self.mockPatternModel[deviceName]

  def getRenderFrames(self):
    frames = {
      "mock": {},
      "real": {}
    }

    # Assume same number of devices in both models
    for key in self.factory.discoSession.patternModel:
      frames[mock][key] = self.mockPatternModel[key].render()
      frames[real][key] = self.factory.discoSession.patternModel[key].render()
    return frames


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