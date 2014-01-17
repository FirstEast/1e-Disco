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

class LinearGradient(StaticPattern):
  DEFAULT_PARAMS = {
    'Vertical': False,
    'StartHue': 0,
    'EndHue': 359
  } # Hues can and should go above 360 if you want wrapping.
  def renderFrame(self, device):
     if self.params['Vertical']:
       wid = device.width
       hei = device.height
     else:
       wid = device.height
       hei = device.width
     huerange = [int(self.params['StartHue'] + (self.params['EndHue'] - self.params['StartHue']) * i / hei) % 360 for i in range(hei)]
     colorArr = [Color((hue, 1, 255), True) for hue in huerange]
     frameRet = Frame([colorArr] * wid)
     if not self.params['Vertical']: frameRet = frameRet.transpose()
     return frameRet
