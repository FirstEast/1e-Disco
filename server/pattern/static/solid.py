from pattern.color import *
from pattern.pattern import *

class SolidColor(StaticPattern):
  DEFAULT_PARAMS = {
    'Color': BLUE
  }
  
  def renderFrame(self, device):
    return Frame([[self.params['Color']] * device.width] * device.height)

class Gradient(StaticPattern):
  # Radial, linear, multicolor.
  # interpolateColors function can help you do this
  # Also make a parameter a color list so you can have N color gradients
  pass