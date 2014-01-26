from pattern.color import *
from pattern.pattern import *
from pattern.importer import *
from pattern.static.shapes import *
from sockets.control import MOCK_DEVICES
from PIL import Image, ImageDraw, ImageFilter

import math
import inspect

class RingsMaker(Pattern):
  DEFAULT_PARAMS = {
    'Pattern': 'sliding_rainbow.json',
    'Size': 20,
    'Rate': 5,
    'CenterX': 24,
    'CenterY': 12
  }

  def paramUpdate(self):
    self.pattern = loadSavedPatternFromFilename(self.beat, self.params['Pattern'])
    if 'Rate' in self.pattern.params: self.pattern.params['Rate'] *= self.params['Rate']

  def render(self, device):
    array = list(self.pattern.render(MOCK_DEVICES['goodale']).getdata())
    ret = Image.new('RGB', (device.width, device.height))
    ret.putdata([array[int(len(array) * math.sqrt(y*y + x*x) / (self.params['Size'])) % len(array)]
      for y in range(-self.params['CenterY'], device.height - self.params['CenterY'])
      for x in range(-self.params['CenterX'], device.width - self.params['CenterX'])])
    return ret

class SpiralMaker(Pattern):
  DEFAULT_PARAMS = {
    'Pattern': 'sliding_rainbow.json',
    'Rate': 5,
    '1000Twist': 15,
    'CenterX': 24,
    'CenterY': 12,
    'Wraps': 1
  }

  def paramUpdate(self):
    self.pattern = loadSavedPatternFromFilename(self.beat, self.params['Pattern'])
    if 'Rate' in self.pattern.params: self.pattern.params['Rate'] *= self.params['Rate']

  def render(self, device):
    array = list(self.pattern.render(MOCK_DEVICES['goodale']).getdata())
    ret = Image.new('RGB', (device.width, device.height))
    func = lambda (x, y): (math.sqrt(y*y + x*x) * self.params['1000Twist'] / 1000.0 + math.atan2(y, x)) * self.params['Wraps'] / (2 * math.pi)
    ret.putdata([array[int(len(array) * func((x, y))) % len(array)]
      for y in range(-self.params['CenterY'], device.height - self.params['CenterY'])
      for x in range(-self.params['CenterX'], device.width - self.params['CenterX'])])
    return ret
  
class DiamondMaker(Pattern):
  DEFAULT_PARAMS = {
    'Pattern': 'sliding_rainbow.json',
    'Size': 20,
    'Rate': 5,
    'CenterX': 24,
    'CenterY': 12
  }

  def paramUpdate(self):
    self.pattern = loadSavedPatternFromFilename(self.beat, self.params['Pattern'])
    if 'Rate' in self.pattern.params: self.pattern.params['Rate'] *= self.params['Rate']

  def render(self, device):
    array = list(self.pattern.render(MOCK_DEVICES['goodale']).getdata())
    ret = Image.new('RGB', (device.width, device.height))
    ret.putdata([array[int(len(array) * (abs(y) + abs(x)) / (self.params['Size'])) % len(array)]
      for y in range(-self.params['CenterY'], device.height - self.params['CenterY'])
      for x in range(-self.params['CenterX'], device.width - self.params['CenterX'])])
    return ret

class RadarMaker(Pattern):
  DEFAULT_PARAMS = {
    'Pattern': 'sliding_rainbow.json',
    'Rate': 5,
    'CenterX': 24,
    'CenterY': 12,
    'Wraps': 1
  }

  def paramUpdate(self):
    self.pattern = loadSavedPatternFromFilename(self.beat, self.params['Pattern'])
    if 'Rate' in self.pattern.params: self.pattern.params['Rate'] *= self.params['Rate'] * self.params['Wraps']

  def render(self, device):
    array = list(self.pattern.render(MOCK_DEVICES['goodale']).getdata())
    ret = Image.new('RGB', (device.width, device.height))
    ret.putdata([array[int(len(array) * self.params['Wraps'] * math.atan2(y, x) / (2 * math.pi)) % len(array)]
      for y in range(-self.params['CenterY'], device.height - self.params['CenterY'])
      for x in range(-self.params['CenterX'], device.width - self.params['CenterX'])])
    return ret

class TrippyAsFuck(Pattern):
  def paramUpdate(self):
    self.pattern = loadSavedPatternFromFilename(self.beat, 'sliding_rainbow.json')

  def render(self, device):
    array = list(self.pattern.render(device).getdata())
    ret = Image.new('RGB', (device.width, device.height))
    ret.putdata([array[int(len(array) * math.atan2(y, x) / (2 * math.pi))]
      for x in range(-(device.width/2), (device.width + 1)/2)
      for y in range(-(device.height/2), (device.height + 1)/2)])
    return ret

class Zoom(Pattern):
  DEFAULT_PARAMS = {
    'Pattern': 'default_line.json',
    'Zoom': 2,
    'Center X': 24,
    'Center Y': 12
  }

  def paramUpdate(self):
    self.pattern = loadSavedPatternFromFilename(self.beat, self.params['Pattern'])

  def render(self, device):
    im = self.pattern.render(device)
    im2 = im.resize((device.width * 2, device.height * 2), Image.ANTIALIAS)

    width, height = im2.size

    left = (width - device.width)/2
    top = (height - device.height)/2
    right = (width + device.width)/2
    bottom = (height + device.height)/2

    return im2.crop((left, top, right, bottom))

class Rotate(Pattern):
  DEFAULT_PARAMS = {
    'Pattern': 'default_line.json',
    'Angle': 120
  }

  def paramUpdate(self):
    self.pattern = loadSavedPatternFromFilename(self.beat, self.params['Pattern'])

  def render(self, device):
    im = self.pattern.render(device)
    im = im.rotate(self.params['Angle'], expand=False).filter(ImageFilter.SMOOTH)

    return im
