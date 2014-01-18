from pattern.color import *
from pattern.pattern import *
from pattern.static.shapes import *
from PIL import Image, ImageDraw, ImageFilter

import inspect

class Zoom(Pattern):
  DEFAULT_PARAMS = {
    'Pattern': Line,
    'Zoom': 2,
    'Center X': 24,
    'Center Y': 12
  }

  def __init__(self, beat, params):
    Pattern.__init__(self, beat, params)

    if inspect.isclass(self.params['Pattern']):
      self.params['Pattern'] = self.params['Pattern'](beat, {})

  def render(self, device):
    im = self.params['Pattern'].render(device)
    im2 = im.resize((device.width * 2, device.height * 2), Image.ANTIALIAS)

    width, height = im2.size

    left = (width - device.width)/2
    top = (height - device.height)/2
    right = (width + device.width)/2
    bottom = (height + device.height)/2

    return im2.crop((left, top, right, bottom))

class Rotate(Pattern):
  DEFAULT_PARAMS = {
    'Pattern': Line,
    'Angle': 120
  }

  def __init__(self, beat, params):
    Pattern.__init__(self, beat, params)

    if inspect.isclass(self.params['Pattern']):
      self.params['Pattern'] = self.params['Pattern'](beat, {})

  def render(self, device):
    im = self.params['Pattern'].render(device)
    im = im.rotate(self.params['Angle'], expand=False).filter(ImageFilter.SMOOTH)

    return im