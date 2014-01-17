from twisted.internet import task
from twisted.internet.protocol import Protocol, ReconnectingClientFactory
from autobahn.twisted.websocket import WebSocketServerProtocol, \
                                WebSocketServerFactory

import json

class AudioWebSocket(WebSocketServerProtocol):
  def onOpen(self):
    self.factory.register(self)

  def connectionLost(self, reason):
    WebSocketServerProtocol.connectionLost(self, reason)
    self.factory.unregister(self)

class AudioWebSocketFactory(WebSocketServerFactory):
  def __init__(self, url, beatData, debug = False, debugCodePaths = False):
    WebSocketServerFactory.__init__(self, url, debug = debug, debugCodePaths = debugCodePaths)
    self.clients = []
    self.beatData = beatData
    task.LoopingCall(self.sendData).start(0.05)

  def sendData(self):
    self.broadcast(json.dumps(self.beatData.__dict__))

  def register(self, client):
    if not client in self.clients:
      self.clients.append(client)

  def unregister(self, client):
    if client in self.clients:
      self.clients.remove(client)

  def broadcast(self, msg):
    for c in self.clients:
      c.sendMessage(msg)

class AudioSocket(Protocol):
  def __init__(self, beatData):
    self.beatData = beatData

  def sendData(self):
    self.sendMessage(json.dumps(self.beatData.__dict__))

  def connectionMade(self):
    print "connected successfully to central server"

  def dataReceived(self, line):
    if "OK" in line:
      self.sendData()

  def sendMessage(self, message):
    self.transport.write(message + '\n')

class AudioSocketFactory(ReconnectingClientFactory):
  def __init__(self, beatData):
    self.beatData = beatData

  def buildProtocol(self, addr):
    self.resetDelay()
    return AudioSocket(self.beatData)

  def clientConnectionLost(self, connector, reason):
    ReconnectingClientFactory.clientConnectionLost(self, connector, reason)

  def clientConnectionFailed(self, connector, reason):
    ReconnectingClientFactory.clientConnectionFailed(self, connector,
                                                     reason)