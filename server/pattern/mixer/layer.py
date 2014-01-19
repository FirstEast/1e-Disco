from pattern.color import *
from pattern.pattern import *
from pattern.importer import *
from pattern.static.shapes import Circle
from pattern.static.solid import LinearRainbow

from PIL import Image, ImageChops

import inspect

def layerPatterns(top, bottom):
    return ImageChops.add(top, maskPatterns(top, bottom, True))

def maskPatterns(mask, patternImg, flip = False):
  maskData = mask.convert('L').getdata()
  patternData = patternImg.getdata()
  
  newData = []
  for i in range(len(maskData)):
    if (maskData[i] > 0) != flip:
      newData.append(patternData[i])
    else:
      newData.append((0, 0, 0))

  patternImg.putdata(newData)
  return patternImg

class LayerPattern(Pattern):
  DEFAULT_PARAMS = {
    'LayerClasses': (Circle, LinearRainbow),
    'Params': ({}, {})
  }

  def __init__(self, beat, params):
    Pattern.__init__(self, beat, params)
    self.params['Layers'] = []
    for i in range(len(self.params['LayerClasses'])):
       clazz = self.params['LayerClasses'][i]
       if inspect.isclass(clazz):
         self.params['Layers'].append(clazz(beat, self.params['Params'][i]))
       else:
         print "Error initializing LayerPattern: LayerClasses parameter must contain only classes"

  def render(self, device):
    current = self.params['Layers'][0].render(device)
    for layer in self.params['Layers'][1:]:
      current = layerPatterns(current, layer.render(device))
    return current

class MaskPattern(Pattern):
  DEFAULT_PARAMS = {
    'Mask': Circle,
    'MaskParams': {},
    'Pattern': LinearRainbow,
    'PatternParams': {}
  }

  def __init__(self, beat, params):
    Pattern.__init__(self, beat, params)

    if inspect.isclass(self.params['Mask']):
      self.params['Mask'] = self.params['Mask'](beat, self.params['MaskParams'])

    if inspect.isclass(self.params['Pattern']):
      self.params['Pattern'] = self.params['Pattern'](beat, self.params['PatternParams'])

  def render(self, device):
    mask = self.params['Mask'].render(device)
    patternImg = self.params['Pattern'].render(device)
    return maskPatterns(mask, patternImg)

class Adding(Pattern):
  def __init__(self, beat, params):
    Pattern.__init__(self, beat, params)
    self.p1 = SolidColor(beat, {})
    self.p2 = SolidColor(beat, {'Color': GREEN})
  
  def render(self, device):
    return ImageChops.add(self.p1.render(device), self.p2.render(device))

class Subtracting(Pattern):
  def __init__(self, beat, params):
    Pattern.__init__(self, beat, params)
    self.p1 = SolidColor(beat, {'Color': WHITE})
    self.p2 = SolidColor(beat, {'Color': GREEN})
  
  def render(self, device):
    return ImageChops.subtract(self.p1.render(device), self.p2.render(device))
