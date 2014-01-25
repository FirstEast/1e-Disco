from pattern.color import *
from pattern.pattern import *
from pattern.util import *
from pattern.importer import loadSavedPatternFromFilename

class VaryParam(TimedPattern):
  
  DEFAULT_PARAMS = {
    'Pattern': 'rainbow_rings.json',
    'Param': 'CenterX',
    'MinValue': 8,
    'MaxValue': 40,
    'BumpRate': 0.7,
    'BounceBack': True
  }

  DEFAULT_PARAMS.update(TimedPattern.DEFAULT_PARAMS)

  def paramUpdate(self):
    self.base = loadSavedPatternFromFilename(self.beat, self.params['Pattern'])
    self.val = float(self.params['MinValue'])
    self.frameCount = 0
    self.forward = 1

  def renderFrame(self, device, frameCount):
    if frameCount != self.frameCount:
      self.frameCount = frameCount
      self.val += (self.params['BumpRate'] * self.forward)
      if self.val > self.params['MaxValue']: self.forward = -1
      if self.val < self.params['MinValue']: self.forward = 1
      self.base.params[self.params['Param']] = int(self.val)
    # this class does not call paramUpdate()
    # therefore it will be of limited use if you have a clever subpattern
    return self.base.render(device)
