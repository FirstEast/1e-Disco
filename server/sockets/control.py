from autobahn.twisted.websocket import WebSocketServerProtocol, \
                                WebSocketServerFactory

from pattern.importer import *
from pattern.util import *

import json

# Oh lawd I apologize
class MockDevice():
  def __init__(self, name, width, height, format='RGB'):
    self.name = name
    self.width = width
    self.height = height
    self.format = format

MOCK_DEVICES = {
  'ddf': MockDevice('ddf', DDF_WIDTH, DDF_HEIGHT),
  'goodale': MockDevice('goodale', GOODALE_WIDTH, GOODALE_HEIGHT),
  'bemis': MockDevice('bemis', BEMIS_WIDTH, BEMIS_HEIGHT)
}

class DiscoControlProtocol(WebSocketServerProtocol):
  def onOpen(self):
    self.factory.register(self)

    self.mockPatternModel = {}
    beat = self.factory.discoSession.beatModel
    for key in self.factory.discoSession.patternModel:
      params = self.factory.discoSession.patternModel[key].params
      self.mockPatternModel[key] = self.factory.discoSession.patternModel[key].__class__(beat, params)

    self.sendInitMessage()
    self.sendDevicesMessage()
    self.sendPatternMessage()

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
      self.sendRenderMessage(binary)
    else:
      self.sendMessage('Unrecognized message type', binary)
      return

  def connectionLost(self, reason):
    WebSocketServerProtocol.connectionLost(self, reason)
    self.factory.unregister(self)

  def performSwap(self, deviceName):
    params = self.mockPatternModel[deviceName].params
    beat = self.factory.discoSession.beatModel
    self.factory.discoSession.patternModel[deviceName] = self.mockPatternModel[deviceName].__class__(beat, params)

  def setMockPattern(self, deviceName, patternData):
    self.setPattern(deviceName, patternData, self.mockPatternModel)

  def setRealPattern(self, deviceName, patternData):
    self.setPattern(deviceName, patternData, self.factory.discoSession.patternModel)

  def setPattern(self, deviceName, patternData, patternModel):
    if patternData['saved']:
      pattern = loadSavedPattern(patternData)
    else:
      patternClass = loadPatternFromModuleClassName(patternData['__module__'] + '_' + patternData['name'])
      pattern = patternClass(self.factory.discoSession.beatModel, patternData['params'])
    patternModel[deviceName] = pattern

  def getCurrentDeviceData(self):
    data = {
      'outputDeviceModel': self.factory.discoSession.outputDeviceModel,
      'inputDeviceModel': self.factory.discoSession.inputDeviceModel
    }
    return data

  def getCurrentPatternData(self):
    realPatternClasses = {}
    realPatternParams = {}
    for key in self.factory.discoSession.patternModel:
      realPatternClasses[key] = self.factory.discoSession.patternModel[key].__class__.__name__
      realPatternParams[key] = self.factory.discoSession.patternModel[key].params

    data = {
      'realPatternParams': realPatternParams,
      'realPatternClasses': realPatternClasses
    }
    return data

  def getRenderFrames(self):
    frames = {'mock': {}, 'real': {}}
    for key in self.factory.discoSession.patternModel:
      try:
        mockFrame = self.mockPatternModel[key].render(MOCK_DEVICES[key])
        frames['mock'][key] = [value for color in mockFrame.getdata() for value in color]
        realFrame = self.factory.discoSession.patternModel[key].render(MOCK_DEVICES[key])
        frames['real'][key] = [value for color in realFrame.getdata() for value in color]
      except Exception, e: 
        print str(e)
    return frames

  def sendInitMessage(self):
    message = {
      'type': 'init',
      'patternListData': getPatternMapJson(),
    }
    self.sendMessage(json.dumps(message, default=(lambda x: x.__dict__)))

  def sendDevicesMessage(self):
    message = {
      'type': 'devices',
      'deviceData': self.getCurrentDeviceData(),
    }
    self.sendMessage(json.dumps(message, default=(lambda x: x.__dict__)))

  def sendPatternMessage(self):
    message = {
      'type': 'realPatternData',
      'patternData': self.getCurrentPatternData(),
    }
    self.sendMessage(json.dumps(message, default=(lambda x: x.__dict__)))

  def sendRenderMessage(self, binary):
    message = {
      'type': 'render',
      'renderData': self.getRenderFrames(),
    }
    self.sendMessage(json.dumps(message, default=(lambda x: x.__dict__)), binary)


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
