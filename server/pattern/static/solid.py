from pattern.color import *
from pattern.pattern import *
from PIL import Image, ImageChops

class SolidColor(StaticPattern):
  DEFAULT_PARAMS = {
    'Color': BLUE
  }
  
  def renderFrame(self, device):
    im = Image.new('RGB', (device.width, device.height))
    im.putdata([self.params['Color'].getRGBValues()] * (device.width * device.height))
    return im

class LinearRainbow(StaticPattern):
  DEFAULT_PARAMS = {
    'Horizontal': True,
    'StartHue': 0.0,
    'EndHue': 1.0,
  } # Hues can and should go above 1 if you want wrapping.

  def renderFrame(self, device):
    if self.params['Horizontal']:
      wid = device.width
      hei = device.height
    else:
      wid = device.height
      hei = device.width
    huerange = [self.params['StartHue'] + (self.params['EndHue'] - self.params['StartHue']) * i / wid for i in range(wid)]
    colorArr = [Color((hue, 1, 255), True).getRGBValues() for hue in huerange]
    im = Image.new('RGB', (wid, hei))
    im.putdata(colorArr * hei)
    if not self.params['Horizontal']: im = im.transpose(ROTATE_270).transpose(FLIP_LEFT_RIGHT)
    return im
