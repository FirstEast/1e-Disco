from pattern.color import *
from pattern.pattern import *
from pattern.importer import *
from pattern.static.shapes import Circle
from pattern.static.solid import LinearRainbow

from PIL import Image, ImageChops

import inspect

class LayerPattern(Pattern):
  pass

class MaskPattern(Pattern):
  DEFAULT_PARAMS = {
    'Mask': Circle,
    'Pattern': LinearRainbow
  }

  def __init__(self, beat, params):
    Pattern.__init__(self, beat, params)
    self.maskPattern = None

    if inspect.isclass(self.params['Mask']):
      self.params['Mask'] = self.params['Mask'](beat, {})

    if inspect.isclass(self.params['Pattern']):
      self.params['Pattern'] = self.params['Pattern'](beat, {})

  def setNextMaskPattern(self, maskPattern):
    self.maskPattern = maskPattern

  def render(self, device):
    mask = self.params['Mask'].render(device)
    patternImg = self.params['Pattern'].render(device)
    return maskPatterns(mask, patternImg)