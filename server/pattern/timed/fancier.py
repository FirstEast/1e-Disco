from pattern.color import *
from pattern.pattern import *
from pattern.util import *
from pattern.importer import loadSavedPatternFromFilename
import math, random

random.seed()

# Whether or not to call paramUpdate() is worth pondering in each case.

class AdjustParam(TimedPattern):
  DEFAULT_PARAMS = {
    'Pattern': 'rect_blue.json',
    'Param': 'Lalala',
    'CallUpdate()': True
  }

  def paramUpdate(self, paramName):
    if paramName == 'ALL':
      self.base = loadSavedPatternFromFilename(self.params['Pattern'])
    elif paramName == 'Pattern':
      self.base = loadSavedPatternFromFilename(self.params['Pattern'])
    elif not(paramName in self.DEFAULT_PARAMS):
      self.base.params[paramName] = self.params[paramName]
      if self.params['CallUpdate()']: self.base.paramUpdate(paramName)
    self.frameCount = 0

  def getVal(self):
    pass
  
  def renderFrame(self, device, frameCount):
    if frameCount != self.frameCount:
      self.frameCount = frameCount
      self.base.params[self.params['Param']] = self.getVal()
      if self.params['CallUpdate()']: self.base.paramUpdate(self.params['Param'])
    return self.base.render(device)

  DEFAULT_PARAMS.update(TimedPattern.DEFAULT_PARAMS)

class RandParamInitInt(AdjustParam):
  DEFAULT_PARAMS = {
    'MinValue': 8,
    'MaxValue': 40
  }

  DEFAULT_PARAMS.update(AdjustParam.DEFAULT_PARAMS)

  def paramUpdate(self, paramName):
    AdjustParam.paramUpdate(self, paramName)
    self.val = random.randint(self.params['MinValue'], self.params['MaxValue'])

  def getVal(self):
    return self.val

class RandParamInitColor(AdjustParam):
  DEFAULT_PARAMS = AdjustParam.DEFAULT_PARAMS

  def paramUpdate(self, paramName):
    AdjustParam.paramUpdate(self, paramName)
    self.val = Color((random.randint(0, 255),
                     random.randint(0, 255),
                     random.randint(0, 255)))
  
  def getVal(self):
    return self.val

class RandParamCycleInt(AdjustParam):
  DEFAULT_PARAMS = {
    'MinValue': 8,
    'MaxValue': 40,
    'FramePeriod': 70,
    'BrownNoise': 0 # if 0, select a random parameter. If n, random walk by up to n each cycle
  }

  DEFAULT_PARAMS.update(AdjustParam.DEFAULT_PARAMS)

  def paramUpdate(self, paramName):
    AdjustParam.paramUpdate(self, paramName)
    self.val = random.randint(self.params['MinValue'], self.params['MaxValue'])

  def getVal(self):
    if self.frameCount % self.params['FramePeriod'] == 0:
      if self.params['BrownNoise'] != 0:
        self.val += random.randint(-self.params['BrownNoise'],self.params['BrownNoise'])
        if self.val > self.params['MaxValue']: self.val = self.params['MaxValue']
        if self.val < self.params['MinValue']: self.val = self.params['MinValue']
      else:
        self.val = random.randint(self.params['MinValue'], self.params['MaxValue'])
    return self.val

class AdjustParamInt(AdjustParam):
  DEFAULT_PARAMS = {
    'MinValue': 8,
    'MaxValue': 40
  }

  DEFAULT_PARAMS.update(AdjustParam.DEFAULT_PARAMS)

class LoopParam(AdjustParamInt):
  
  DEFAULT_PARAMS = {
    '10ParamRate': 70,
    'BounceBack': True,
    'StartForward': True,
    'Offset': 0
  }

  DEFAULT_PARAMS.update(AdjustParamInt.DEFAULT_PARAMS)

  def paramUpdate(self, paramName):
    AdjustParamInt.paramUpdate(self, paramName)
    self.val = float(self.params['MinValue']) if self.params['StartForward'] else float(self.params['MaxValue'])
    self.val += self.params['Offset']
    self.forward = 1 if self.params['StartForward'] else -1

  def getVal(self):
    self.val += (self.params['10ParamRate'] * self.forward / 10.0)
    if self.val > self.params['MaxValue']:
      if self.params['BounceBack']: self.forward = -1
      else: self.val = self.params['MinValue']
    if self.val < self.params['MinValue']:
      if self.params['BounceBack']: self.forward = 1
      else: self.val = self.params['MaxValue']
    return int(self.val)

class SinuParam(AdjustParamInt):
  
  DEFAULT_PARAMS = {
    'FramePeriod': 70,
    'DegPhase': 0
  }

  DEFAULT_PARAMS.update(AdjustParamInt.DEFAULT_PARAMS)

  def getVal(self):
    return int(self.params['MinValue'] + (self.params['MaxValue'] - self.params['MinValue']) * (1 + math.sin((self.params['DegPhase'] * 2 * math.pi / 360.0) + self.frameCount * 2 * math.pi / self.params['FramePeriod'])) / 2)

class AlterParamInt(AdjustParamInt):
  
  DEFAULT_PARAMS = {
    'FramePeriod': 70,
    'Offset': False
  }

  DEFAULT_PARAMS.update(AdjustParamInt.DEFAULT_PARAMS)

  def getVal(self):
    if ((self.frameCount / self.params['FramePeriod']) % 2 == 0) == self.params['Offset']: return self.params['MinValue']
    else: return self.params['MaxValue']

class AlterParamBool(AdjustParam):
  
  DEFAULT_PARAMS = {
    'FramePeriod': 70,
    'Offset': False
  }

  DEFAULT_PARAMS.update(AdjustParam.DEFAULT_PARAMS)

  def getVal(self):
    return ((self.frameCount / self.params['FramePeriod']) % 2 == 0) == self.params['Offset']
