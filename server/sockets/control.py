from autobahn.twisted.websocket import WebSocketServerProtocol, \
                                WebSocketServerFactory

from pattern.importer import *
from pattern.util import *
from pattern.color import *
from pattern.pattern import TimedPattern

import json
import traceback

# Create mock devices since render requires a device (instead of using the socket)
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
    for key in self.factory.discoSession.patternModel:
      params = self.factory.discoSession.patternModel[key].params
      self.mockPatternModel[key] = self.factory.discoSession.patternModel[key].__class__(params)

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
    elif msgType == 'realParam':
      self.setRealPatternParam(data['deviceName'], data['paramName'], data['paramVal'])
    elif msgType == 'mockParam':
      self.setMockPatternParam(data['deviceName'], data['paramName'], data['paramVal'])
    elif msgType == 'render':
      self.sendRenderMessage(binary)
    elif msgType == 'audio':
      self.sendAudioMessage(binary)
    else:
      self.sendMessage('Unrecognized message type', binary)
      return

  def connectionLost(self, reason):
    WebSocketServerProtocol.connectionLost(self, reason)
    self.factory.unregister(self)

  def setMockPattern(self, deviceName, patternData):
    self.setPattern(deviceName, patternData, self.mockPatternModel)

  def setRealPattern(self, deviceName, patternData):
    self.setPattern(deviceName, patternData, self.factory.discoSession.patternModel)

  def setPattern(self, deviceName, patternData, patternModel):
    if patternData['saved']:
      pattern = loadSavedPattern(patternData)
    else:
      patternClass = loadPatternFromModuleClassName(patternData['__module__'] + '_' + patternData['name'])
      pattern = patternClass(sanitizeParams(patternData['params']))
    patternModel[deviceName] = pattern

  def savePattern(self, patternData):
    name = str(patternData['saveName'])

    f = open(PATTERN_SAVE_DIR + name + '.json','w')
    json.dump(patternData, f)
    f.close()

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
        if key == 'goodale' and self.mockPatternModel[key].__class__.__name__ == 'MimicPattern':
          mockFrame = unflattenGoodaleArray(flatGoodaleArrayFromDdfImage(self.mockPatternModel['ddf'].render(MOCK_DEVICES['ddf'])))
        else:
          mockFrame = self.mockPatternModel[key].render(MOCK_DEVICES[key])
        frames['mock'][key] = [value for color in mockFrame.getdata() for value in color]

        if key == 'goodale' and self.factory.discoSession.patternModel[key].__class__.__name__ == 'MimicPattern':
          realFrame = unflattenGoodaleArray(flatGoodaleArrayFromDdfImage(self.factory.discoSession.getPattern('ddf').render(MOCK_DEVICES['ddf'])))
        else:
          realFrame = self.factory.discoSession.patternModel[key].render(MOCK_DEVICES[key])
        frames['real'][key] = [value for color in realFrame.getdata() for value in color]
      except Exception, e:
        traceback.print_stack()
        print str(e)
    return frames

  def setRealPatternParam(self, device, name, value):
    param = sanitizeParams({name: value})
    self.factory.discoSession.getPattern(device).setParam(name, param[name])

  def setMockPatternParam(self, device, name, value):
    param = sanitizeParams({name: value})
    self.mockPatternModel[device].setParam(name, param[name])

  def sendInitMessage(self):
    message = {
      'type': 'init',
      'patternListData': getPatternMapJson(),
      'savedPatternListData': getSavedPatternJson(),
      'gifList': getGifList(),
      'imageList': getImageList()
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

  def sendAudioMessage(self, binary):
    message = {
      'type': 'audio',
      'audioData': {
        'volume': BEAT_MODEL.avgVolume,
        'centroid': BEAT_MODEL.avgCentroid,
        'frequencies': BEAT_MODEL.avgFreqs
      }
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
