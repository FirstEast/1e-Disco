from autobahn.twisted.websocket import WebSocketServerProtocol, \
                                WebSocketServerFactory

from pattern.importer import *

import json
import copy

# Don't deep copy without copying the same BeatModel over from the session.
# Otherwise, bad times will happen.

class DiscoControlProtocol(WebSocketServerProtocol):
  def onOpen(self):
    self.factory.register(self)
    self.sendMessage(getPatternMapJson())

    for key in self.factory.discoSession.patternModel:
      self.mockPatternModel[key] = copy.deepcopy(self.factory.discoSession.patternModel[key])
      self.mockPatternModel[key].beat = self.factory.discoSession.beatModel

  def onMessage(self, msg, binary):
    data = json.loads(msg.strip())
    msgType = data['type']

    if msgType == 'setMockPattern':
      self.setMockPattern(data['deviceName'], data['patternData'])
    elif msgType == 'setRealPattern':
      self.setRealPattern(data['deviceName'], data['patternData'])
    elif msgType == 'savePattern':
      self.savePattern(data['patternData'])
    elif msgType == 'swapPattern':
      self.performSwap(data['deviceName'])
    elif msgType == 'render':
      self.sendMessage(json.dumps(self.getRenderFrames()), binary)
    else:
      self.sendMessage('Unrecognized message type', binary)
      return

    self.sendMessage('OK', binary)

  def connectionLost(self, reason):
    WebSocketServerProtocol.connectionLost(self, reason)
    self.factory.unregister(self)

  def performSwap(self, deviceName):
    self.factory.discoSession.patternModel[deviceName] = copy.deepcopy(self.mockPatternModel[deviceName])
    self.factory.discoSession.patternModel[deviceName].beat = self.factory.discoSession.beatModel

  def setMockPattern(self, deviceName, patternData):
    self.setPattern(deviceName, patternData, self.mockPatternModel)

  def setRealPattern(self, deviceName, patternData):
    self.setPattern(deviceName, patternData, self.factory.discoSession.patternModel)

  def setPattern(self, deviceName, patternData, patternModel):
    if patternData['saved']:
      pattern = loadSavedPattern(patternData)
    else:
      patternClass = loadPatternFromModuleClassName(patternData['moduleClassName'])
      pattern = patternClass(self.factory.discoSession.beatModel, patternData['params'])
    patternModel[deviceName] = pattern

  def getRenderFrames(self):
    frames = {
      'mock': {},
      'real': {}
    }

    for key in self.factory.discoSession.patternModel:
      frames['mock'][key] = self.mockPatternModel[key].render()
      frames['real'][key] = self.factory.discoSession.patternModel[key].render()
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
