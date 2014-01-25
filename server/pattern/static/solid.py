from pattern.color import *
from pattern.pattern import *
from PIL import Image, ImageChops

class Checkerboard(StaticPattern):
  DEFAULT_PARAMS = {
    'Color 1': BLACK,
    'Color 2': WHITE,
    'Grain': 3,
    'Offset': False
  }

  def renderFrame(self, device):
    im = Image.new('RGB', (device.width, device.height))
    im.putdata([self.params['Color 1'].getRGBValues()
      if ((y / self.params['Grain'] % 2) != (x / self.params['Grain'] % 2)) != self.params['Offset']
      else self.params['Color 2'].getRGBValues()
      for y in range(device.height) for x in range(device.width)])
    return im

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
    if not self.params['Horizontal']: im = im.transpose(Image.ROTATE_270).transpose(Image.FLIP_LEFT_RIGHT)
    return im
