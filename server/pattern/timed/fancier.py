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

  def paramUpdate(self):
    self.base = loadSavedPatternFromFilename(self.beat, self.params['Pattern'])
    self.frameCount = 0

  def getVal(self):
    pass
  
  def renderFrame(self, device, frameCount):
    if frameCount != self.frameCount:
      self.frameCount = frameCount
      self.base.params[self.params['Param']] = self.getVal()
      if self.params['CallUpdate()']: self.base.paramUpdate()
    return self.base.render(device)

  DEFAULT_PARAMS.update(TimedPattern.DEFAULT_PARAMS)

class RandParamInitInt(AdjustParam):
  DEFAULT_PARAMS = {
    'MinValue': 8,
    'MaxValue': 40
  }

  DEFAULT_PARAMS.update(AdjustParam.DEFAULT_PARAMS)

  def paramUpdate(self):
    AdjustParam.paramUpdate(self)
    self.val = random.randint(self.params['MinValue'], self.params['MaxValue'])

  def getVal(self):
    return self.val

class RandParamInitColor(AdjustParam):
  DEFAULT_PARAMS = AdjustParam.DEFAULT_PARAMS

  def paramUpdate(self):
    AdjustParam.paramUpdate(self)
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

  def paramUpdate(self):
    AdjustParam.paramUpdate(self)
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
    'StartForward': True
  }

  DEFAULT_PARAMS.update(AdjustParamInt.DEFAULT_PARAMS)

  def paramUpdate(self):
    AdjustParamInt.paramUpdate(self)
    self.val = float(self.params['MinValue']) if self.params['StartForward'] else float(self.params['MaxValue'])
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
    'FramePeriod': 70
  }

  DEFAULT_PARAMS.update(AdjustParamInt.DEFAULT_PARAMS)

  def getVal(self):
    return self.params['MinValue'] + (self.params['MaxValue'] - self.params['MinValue']) * (1 + math.sin(self.frameCount * 2 * math.pi / self.params['FramePeriod'])) / 2

class AlterParamInt(AdjustParamInt):
  
  DEFAULT_PARAMS = {
    'FramePeriod': 70
  }

  DEFAULT_PARAMS.update(AdjustParamInt.DEFAULT_PARAMS)

  def getVal(self):
    if (self.frameCount / self.params['FramePeriod']) % 2 == 0: return self.params['MinValue']
    else: return self.params['MaxValue']

class AlterParamBool(AdjustParam):
  
  DEFAULT_PARAMS = {
    'FramePeriod': 70
  }

  DEFAULT_PARAMS.update(AdjustParam.DEFAULT_PARAMS)

  def getVal(self):
    return (self.frameCount / self.params['FramePeriod']) % 2 == 0
