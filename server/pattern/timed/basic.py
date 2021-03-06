from pattern.color import *
from pattern.pattern import *
from pattern.util import *
from pattern.importer import loadSavedPatternFromFilename

class Interpolation(TimedPattern):

  DEFAULT_PARAMS = {
    'Color 1': RED,
    'Color 2': GREEN,
    'Color 3': BLUE,
  }

  DEFAULT_PARAMS.update(TimedPattern.DEFAULT_PARAMS)

  def paramUpdate(self, paramName):
    self.loop = []
    self.loop += interpolateColors(self.params['Color 1'], self.params['Color 2'])
    self.loop += interpolateColors(self.params['Color 2'], self.params['Color 3'])
    self.loop += interpolateColors(self.params['Color 3'], self.params['Color 1'])

  def renderFrame(self, device, frameCount):
    count = frameCount % len(self.loop)
    frame = [self.loop[count].getRGBValues()] * (device.width * device.height)
    im = Image.new('RGB', (device.width, device.height))
    im.putdata(frame)
    return im

class MovingAnything(TimedPattern):
  DEFAULT_PARAMS = {
    'Base Pattern': 'default_linrainbow.json',
    'X Rate': 1,
    'Y Rate': 0
  }

  DEFAULT_PARAMS.update(TimedPattern.DEFAULT_PARAMS)

  def paramUpdate(self, paramName):
    if paramName == 'ALL':
      self.base = loadSavedPatternFromFilename(self.params['Base Pattern'])
    elif paramName == 'Base Pattern':
      self.base = loadSavedPatternFromFilename(self.params['Base Pattern'])

  def renderFrame(self, device, frameCount):
    return self.base.render(device).offset(int(self.params['X Rate'] * frameCount),
                                           int(self.params['Y Rate'] * frameCount))

class Strobe(TimedPattern):

  DEFAULT_PARAMS = {
    'Color': WHITE
  }

  DEFAULT_PARAMS.update(TimedPattern.DEFAULT_PARAMS)

  def renderFrame(self, device, frameCount):
    count = frameCount % 2

    color = self.params['Color']
    if count == 0:
      color = BLACK

    frame = [color.getRGBValues()] * (device.width * device.height)
    im = Image.new('RGB', (device.width, device.height))
    im.putdata(frame)
    return im