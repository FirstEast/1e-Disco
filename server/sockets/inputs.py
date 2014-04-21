from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from autobahn.twisted.websocket import WebSocketServerProtocol, \
                                WebSocketServerFactory

from pattern.util import BEAT_MODEL
from pattern.util import KEY_MODEL

import json

class BeatServerReceiver(LineReceiver):
  def __init__(self, discoSession):
    self.discoSession = discoSession
    self.beatModel = BEAT_MODEL

  def connectionMade(self):
    self.discoSession.inputDeviceModel["beat"] = True
    self.sendMessage("OK")

  def connectionLost(self, reason):
    self.discoSession.inputDeviceModel["beat"] = False

  def dataReceived(self, line):
    data = json.loads(line.strip())
    self.beatModel.updateData(data['centroid'], data['volume'], data['frequencies'])
    self.sendMessage("OK")

  def sendMessage(self, message):
    self.transport.write(message + '\n')

class BeatServerReceiverFactory(Factory):
  def __init__(self, discoSession):
    self.discoSession = discoSession

  def buildProtocol(self, addr):
    return BeatServerReceiver(self.discoSession)

class KeyInputProtocol(WebSocketServerProtocol):
  def onOpen(self):
    self.factory.discoSession.inputDeviceModel["key"] = True

  def onMessage(self, msg, binary):
    data = json.loads(msg.strip())
    msgType = data['type']

    if msgType == 'downKey':
      KEY_MODEL.downKey(data["key"])
    elif msgType == 'upKey':
      KEY_MODEL.upKey(data["key"])

  def connectionLost(self, reason):
    WebSocketServerProtocol.connectionLost(self, reason)
    self.factory.discoSession.inputDeviceModel["key"] = False

class KeyInputSocketFactory(WebSocketServerFactory):
  def __init__(self, url, discoSession, debug = False, debugCodePaths = False):
    WebSocketServerFactory.__init__(self, url, debug = debug, debugCodePaths = debugCodePaths)
    self.clients = []
    self.discoSession = discoSession