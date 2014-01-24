from pattern.color import *
from pattern.pattern import *
from pattern.importer import *
from pattern.static.shapes import Circle
from pattern.static.solid import *

from PIL import Image, ImageChops

import inspect

def layerPatterns(top, bottom, mask = -1, flip = True): # by default, mask's black is the bottom layer
  if mask == -1: mask = top
  topData = top.getdata()
  maskData = mask.convert('L').getdata()
  botData = bottom.getdata()
  
  newData = []
  for i in range(len(maskData)):
    if (maskData[i] > 0) != flip:
      newData.append(botData[i])
    else:
      newData.append(topData[i])
  ret = bottom.copy()
  ret.putdata(newData)
  return ret

def maskPatterns(mask, patternImg): # mask's light is what to keep
  mask = mask.convert('L')
  return layerPatterns(mask, patternImg, mask, False)

class LayerPattern(Pattern):
  DEFAULT_PARAMS = {
    'Top': 'default_circle.json',
    'Bottom': 'default_interpolation.json'
  }

  def __init__(self, beat, params):
    Pattern.__init__(self, beat, params)
    self.topPattern = loadSavedPatternFromFilename(self.beat, self.params['Top'])
    self.botPattern = loadSavedPatternFromFilename(self.beat, self.params['Bottom'])

  def render(self, device):
    return layerPatterns(self.topPattern.render(device), self.botPattern.render(device))

class MaskPattern(Pattern):
  DEFAULT_PARAMS = {
    'Mask': 'default_circle.json',
    'Pattern': 'default_linrainbow.json',
  }

  def paramUpdate(self):
    self.maskPattern = loadSavedPatternFromFilename(self.beat, self.params['Mask'])
    self.bottomPattern = loadSavedPatternFromFilename(self.beat, self.params['Pattern'])

  def render(self, device):
    mask = self.maskPattern.render(device)
    patternImg = self.bottomPattern.render(device)
    return maskPatterns(mask, patternImg)

class Adding(Pattern):
  DEFAULT_PARAMS = {
    'Pattern 1': 'default_circle.json',
    'Pattern 2': 'default_interpolation.json',
  }

  def paramUpdate(self):
    self.p1 = loadSavedPatternFromFilename(self.beat, self.params['Pattern 1'])
    self.p2 = loadSavedPatternFromFilename(self.beat, self.params['Pattern 2'])
  
  def render(self, device):
    return ImageChops.add(self.p1.render(device), self.p2.render(device))

class Subtracting(Pattern):
  DEFAULT_PARAMS = {
    'Pattern 1': 'default_circle.json',
    'Pattern 2': 'default_interpolation.json',
  }

  def paramUpdate(self):
    self.p1 = loadSavedPatternFromFilename(self.beat, self.params['Pattern 1'])
    self.p2 = loadSavedPatternFromFilename(self.beat, self.params['Pattern 2'])
  
  def render(self, device):
    return ImageChops.subtract(self.p1.render(device), self.p2.render(device))
