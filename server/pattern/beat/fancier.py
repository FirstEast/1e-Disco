from pattern.color import *
from pattern.pattern import *
from pattern.util import *
from pattern.mixer.layer import *
from pattern.importer import *

SMOOTHING_ALPHA = 0.8

class BeatAdjustParam(Pattern):
  DEFAULT_PARAMS = {
    'Pattern': 'rect_blue.json',
    'Param': 'Lalala',
    'CallUpdate': False
  }

  USE_BEAT = True

  def paramUpdate(self, paramName):
    if paramName == 'ALL':
      self.base = loadSavedPatternFromFilename(self.beat, self.params['Pattern'])
    elif paramName == 'Pattern':
      self.base = loadSavedPatternFromFilename(self.beat, self.params['Pattern'])
    elif not(paramName in self.DEFAULT_PARAMS):
      self.base.params[paramName] = self.params[paramName]
      if self.params['CallUpdate()']: self.base.paramUpdate(paramName)

  def getVal(self):
    pass
  
  def render(self, device):
    self.base.params[self.params['Param']] = self.getVal()
    if self.params['CallUpdate']: self.base.paramUpdate(self.params['Param'])
    return self.base.render(device)

class BeatAdjustParamIntAvgVolume(BeatAdjustParam):
  DEFAULT_PARAMS = {
    'MinValue': 8,
    'MaxValue': 40
  }

  DEFAULT_PARAMS.update(BeatAdjustParam.DEFAULT_PARAMS)

  def paramUpdate(self, paramName):
    BeatAdjustParam.paramUpdate(self, paramName)
    self.val = self.getVal()

  def getVal(self):
    self.val = scaleToBucket(self.beat.avgVolume, self.params['MinValue'], self.params['MaxValue'])
    return self.val

class BeatAdjustParamIntAvgCentroid(BeatAdjustParam):
  DEFAULT_PARAMS = {
    'MinValue': 8,
    'MaxValue': 40,
    'AutoScale': True
  }

  DEFAULT_PARAMS.update(BeatAdjustParam.DEFAULT_PARAMS)

  def paramUpdate(self, paramName):
    BeatAdjustParam.paramUpdate(self, paramName)
    self.val = self.getVal()

  def getVal(self):
    val = self.beat.avgCentroid
    if self.params['AutoScale']:
      val = max(self.beat.avgCentroid - 0.5, 0) * 2
    self.val = scaleToBucket(val, self.params['MinValue'], self.params['MaxValue'])
    return self.val

class BeatAdjustParamIntFrequencySum(BeatAdjustParam):
  DEFAULT_PARAMS = {
    'MinValue': 8,
    'MaxValue': 40,
    'Frequency Start': 0,
    'Frequency End': 8  
  }

  DEFAULT_PARAMS.update(BeatAdjustParam.DEFAULT_PARAMS)

  def paramUpdate(self, paramName):
    BeatAdjustParam.paramUpdate(self, paramName)
    freqData = getSummedFreqData(self.beat, self.params['Frequency Start'], self.params['Frequency End'])
    self.val = scaleToBucket(freqData, self.params['MinValue'], self.params['MaxValue'])

  def getVal(self):
    freqData = getSummedFreqData(self.beat, self.params['Frequency Start'], self.params['Frequency End'])
    oldVal = self.val
    newVal = scaleToBucket(freqData, self.params['MinValue'], self.params['MaxValue'])
    self.val = int(newVal * SMOOTHING_ALPHA + oldVal * (1 - SMOOTHING_ALPHA))
    return self.val
