from pattern.color import *
from pattern.util import *
from pattern.pattern import *
from pattern.importer import *
from pattern.static.shapes import *
from sockets.control import MOCK_DEVICES
from PIL import Image, ImageDraw, ImageFilter

import math

class TrivialPattern(Pattern):
  DEFAULT_PARAMS = {
    'Pattern': 'sliding_rainbow.json'
  }

  def paramUpdate(self, paramName):
    self.pattern = loadSavedPatternFromFilename(self.params['Pattern'])

  def render(self, device):
    return self.pattern.render(device)

class MimicPattern(Pattern):
  DEVICES = ['goodale']

class HSVFilter(Pattern):
  DEFAULT_PARAMS = {
    'Pattern': 'sliding_rainbow.json',
    '100dH': 0, # hue shift
    '100dS': 0, # percent saturation shift
    '100dV': 0  # percent value shift
  }

  def paramUpdate(self, paramName):
    if paramName == 'Pattern' or paramName == 'ALL':
      self.pattern = loadSavedPatternFromFilename(self.params['Pattern'])

  def render(self, device):
    def change(x):
      return HSV_shift(x,
        self.params['100dH'] / 100.0,
        self.params['100dS'] / 100.0,
        self.params['100dV'] / 100.0)
    fr = self.pattern.render(device)
    fr.putdata(map(change, fr.getdata()))
    return fr

class HSVKeyFilter(Pattern):
  DEFAULT_PARAMS = {
    'Pattern': 'sliding_rainbow.json'
  }

  def paramUpdate(self, paramName):
    if paramName == 'Pattern' or paramName == 'ALL':
      self.pattern = loadSavedPatternFromFilename(self.params['Pattern'])

  def render(self, device):
    shift = (0, 0, 0)
    if KEY_MODEL.newestKey != None:
      shift = KEY_HSV_SHIFT_MAPPING[KEY_MODEL.newestKey]
    def change(x):
      return HSV_shift(x,
        shift[0] / 100.0,
        shift[1] / 100.0,
        shift[2] / 100.0)
    fr = self.pattern.render(device)
    fr.putdata(map(change, fr.getdata()))
    return fr

class RingsMaker(Pattern):
  DEFAULT_PARAMS = {
    'Pattern': 'sliding_rainbow.json',
    'Size': 20,
    'Rate': 30,
    'CenterX': DDF_WIDTH / 2,
    'CenterY': DDF_HEIGHT / 2
  }

  def paramUpdate(self, paramName):
    if paramName == 'ALL':
      self.pattern = loadSavedPatternFromFilename(self.params['Pattern'])
      self.pattern.params['Rate'] = self.params['Rate']
    elif paramName == 'Pattern':
      self.pattern = loadSavedPatternFromFilename(self.params['Pattern'])
    elif paramName == 'Rate':
      self.pattern.params['Rate'] = self.params['Rate']

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
    'Rate': 30,
    '1000Twist': 15,
    'CenterX': DDF_WIDTH / 2,
    'CenterY': DDF_HEIGHT / 2,
    'Wraps': 1
  }

  def paramUpdate(self, paramName):
    if paramName == 'ALL':
      self.pattern = loadSavedPatternFromFilename(self.params['Pattern'])
      self.pattern.params['Rate'] = self.params['Rate']
    elif paramName == 'Pattern':
      self.pattern = loadSavedPatternFromFilename(self.params['Pattern'])
    elif paramName == 'Rate':
      self.pattern.params['Rate'] = self.params['Rate']

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
    'Rate': 30,
    'CenterX': DDF_WIDTH / 2,
    'CenterY': DDF_HEIGHT / 2
  }

  def paramUpdate(self, paramName):
    if paramName == 'ALL':
      self.pattern = loadSavedPatternFromFilename(self.params['Pattern'])
      self.pattern.params['Rate'] = self.params['Rate']
    elif paramName == 'Pattern':
      self.pattern = loadSavedPatternFromFilename(self.params['Pattern'])
    elif paramName == 'Rate':
      self.pattern.params['Rate'] = self.params['Rate']

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
    'Rate': 30,
    'CenterX': DDF_WIDTH / 2,
    'CenterY': DDF_HEIGHT / 2,
    'Wraps': 1
  }

  def paramUpdate(self, paramName):
    if paramName == 'ALL':
      self.pattern = loadSavedPatternFromFilename(self.params['Pattern'])
      self.pattern.params['Rate'] = self.params['Rate']
    elif paramName == 'Pattern':
      self.pattern = loadSavedPatternFromFilename(self.params['Pattern'])
    elif paramName == 'Rate':
      self.pattern.params['Rate'] = self.params['Rate']

  def render(self, device):
    array = list(self.pattern.render(MOCK_DEVICES['goodale']).getdata())
    ret = Image.new('RGB', (device.width, device.height))
    ret.putdata([array[int(len(array) * self.params['Wraps'] * math.atan2(y, x) / (2 * math.pi)) % len(array)]
      for y in range(-self.params['CenterY'], device.height - self.params['CenterY'])
      for x in range(-self.params['CenterX'], device.width - self.params['CenterX'])])
    return ret

class TrippyAsFuck(Pattern):
  def paramUpdate(self, paramName):
    self.pattern = loadSavedPatternFromFilename('sliding_rainbow.json')

  def render(self, device):
    array = list(self.pattern.render(device).getdata())
    ret = Image.new('RGB', (device.width, device.height))
    ret.putdata([array[int(len(array) * math.atan2(y, x) / (2 * math.pi))]
      for x in range(-(device.width/2), (device.width + 1)/2)
      for y in range(-(device.height/2), (device.height + 1)/2)])
    return ret
