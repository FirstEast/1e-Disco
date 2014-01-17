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

    if inspect.isclass(self.params['Mask']):
      self.params['Mask'] = self.params['Mask'](beat, {})

    if inspect.isclass(self.params['Pattern']):
      self.params['Pattern'] = self.params['Pattern'](beat, {})

  def render(self, device):
    mask = self.params['Mask'].render(device)
    maskData = mask.convert('L').getdata()
    patternImg = self.params['Pattern'].render(device)
    patternData = patternImg.getdata()

    newData = []
    for i in range(len(maskData)):
      if maskData[i] > 0:
        newData.append(patternData[i])
      else:
        newData.append((0, 0, 0))

    patternImg.putdata(newData)
    return patternImg