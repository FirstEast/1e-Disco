from pattern.color import *
from pattern.pattern import *
from pattern.importer import *
from pattern.util import *
from pattern.static.shapes import Circle
from pattern.static.solid import *
from pattern.importer import loadSavedPatternFromFilename
from sockets.control import MockDevice

from PIL import Image, ImageChops

import inspect

class TilePattern(Pattern):
  DEFAULT_PARAMS = {
    'X Segments': 4,
    'Y Segments': 1,
    'Pattern': 'default_linrainbow.json'
  }

  def paramUpdate(self):
    self.pats = [[loadSavedPatternFromFilename(self.beat, self.params['Pattern'])
      for x in range(self.params['X Segments'])]
      for y in range(self.params['Y Segments'])]

  def render(self, device):
    lwid = device.width / self.params['X Segments']
    lhei = device.height / self.params['Y Segments']
    self.mockDevice = MockDevice("segmented pattern", lwid, lhei)
    ret = Image.new('RGB', (device.width, device.height))
    for y in range(self.params['Y Segments']):
      for x in range(self.params['X Segments']):
        ret.paste(self.pats[y][x].render(self.mockDevice), (x * lwid, y * lhei))
    return ret

class LayerPattern(Pattern):
  DEFAULT_PARAMS = {
    'Top': 'default_circle.json',
    'Bottom': 'default_interpolation.json',
    'Mask': 'masks_1e.json',
    'UseMask': False,
    'FlipMask': True
  }

  def paramUpdate(self):
    self.topPattern = loadSavedPatternFromFilename(self.beat, self.params['Top'])
    self.botPattern = loadSavedPatternFromFilename(self.beat, self.params['Bottom'])
    if self.params['UseMask']: self.maskPattern = loadSavedPatternFromFilename(self.beat, self.params['Mask'])

  def render(self, device):
    if self.params['UseMask']:
      return layerPatterns(self.topPattern.render(device), self.botPattern.render(device), self.maskPattern.render(device), self.params['FlipMask'])
    else:
      return layerPatterns(self.topPattern.render(device), self.botPattern.render(device))

class MaskPattern(Pattern):
  DEFAULT_PARAMS = {
    'Mask': 'default_circle.json',
    'Pattern': 'default_linrainbow.json',
  }

  def paramUpdate(self):
    self.maskPattern = loadSavedPatternFromFilename(self.beat, self.params['Mask'])
    self.bottomPattern = loadSavedPatternFromFilename(self.beat, self.params['Pattern'])

  def render(self, device):
    mask = self.maskPattern.render(device)
    patternImg = self.bottomPattern.render(device)
    return maskPatterns(mask, patternImg)

class BlendPattern(Pattern):
  DEFAULT_PARAMS = {
    'Top': 'default_circle.json',
    'Bottom': 'default_interpolation.json',
    'Mask': 'masks_1e.json',
  }

  def paramUpdate(self):
    self.topPattern = loadSavedPatternFromFilename(self.beat, self.params['Top'])
    self.botPattern = loadSavedPatternFromFilename(self.beat, self.params['Bottom'])
    self.maskPattern = loadSavedPatternFromFilename(self.beat, self.params['Mask'])

  def render(self, device):
      return Image.composite(self.topPattern.render(device), self.botPattern.render(device), self.maskPattern.render(device).convert('L'))

class Blending(Pattern):
  DEFAULT_PARAMS = {
    'Pattern 1': 'default_circle.json',
    'Pattern 2': 'default_interpolation.json',
    '100Weight': 50
  }

  def paramUpdate(self):
    self.p1 = loadSavedPatternFromFilename(self.beat, self.params['Pattern 1'])
    self.p2 = loadSavedPatternFromFilename(self.beat, self.params['Pattern 2'])
  
  def render(self, device):
    return ImageChops.blend(self.p1.render(device), self.p2.render(device), self.params['100Weight'] / 100.0)

class Adding(Pattern):
  DEFAULT_PARAMS = {
    'Pattern 1': 'default_circle.json',
    'Pattern 2': 'default_interpolation.json',
  }

  def paramUpdate(self):
    self.p1 = loadSavedPatternFromFilename(self.beat, self.params['Pattern 1'])
    self.p2 = loadSavedPatternFromFilename(self.beat, self.params['Pattern 2'])
  
  def render(self, device):
    return ImageChops.add(self.p1.render(device), self.p2.render(device))

class Subtracting(Pattern):
  DEFAULT_PARAMS = {
    'Pattern 1': 'default_circle.json',
    'Pattern 2': 'default_interpolation.json',
  }

  def paramUpdate(self):
    self.p1 = loadSavedPatternFromFilename(self.beat, self.params['Pattern 1'])
    self.p2 = loadSavedPatternFromFilename(self.beat, self.params['Pattern 2'])
  
  def render(self, device):
    return ImageChops.subtract(self.p1.render(device), self.p2.render(device))
