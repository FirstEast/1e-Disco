from pattern.color import *
from pattern.pattern import *
from pattern.util import *
from pattern.importer import loadSavedPatternFromFilename

class Interpolation(TimedPattern):

  DEFAULT_PARAMS = {
    'Colors': [RED, GREEN, BLUE],
  }

  DEFAULT_PARAMS.update(TimedPattern.DEFAULT_PARAMS)

  def paramUpdate(self):
    self.loop = []
    colors = self.params['Colors'] + [self.params['Colors'][0]]
    for i in range(len(self.params['Colors'])):
      self.loop += interpolateColors(colors[i], colors[i+1])

  def renderFrame(self, device, frameCount):
    count = frameCount % len(self.loop)
    frame = [self.loop[count].getRGBValues()] * (device.width * device.height)
    im = Image.new('RGB', (device.width, device.height))
    im.putdata(frame)
    return im

class MovingAnything(TimedPattern):
  DEFAULT_PARAMS = {
    'Base Pattern': 'default_linrainbow.json',
    'X Rate': 1.0,
    'Y Rate': 0.0
  }

  DEFAULT_PARAMS.update(TimedPattern.DEFAULT_PARAMS)

  def paramUpdate(self):
    self.base = loadSavedPatternFromFilename(self.beat, self.params['Base Pattern'])

  def renderFrame(self, device, frameCount):
    return self.base.render(device).offset(int(self.params['X Rate'] * frameCount),
                                           int(self.params['Y Rate'] * frameCount))

class MovingLight(TimedPattern):

  DEFAULT_PARAMS = {
    'Color': BLUE,
  }

  DEFAULT_PARAMS.update(TimedPattern.DEFAULT_PARAMS)

  DEVICES = ['goodale', 'bemis']

  def renderFrame(self, device, frameCount):
    count = frameCount % device.width
    frame = [(0, 0, 0)] * count
    frame = frame + [self.params['Color'].getRGBValues()]
    frame = frame + [(0, 0, 0)] * (device.width - 1 - count)
    im = Image.new('RGB', (device.width, 1))
    im.putdata(frame)
    return im

class MovingLine(TimedPattern):

  DEFAULT_PARAMS = {
    'Color': BLUE,
  }

  DEFAULT_PARAMS.update(TimedPattern.DEFAULT_PARAMS)

  DEVICES = ['ddf']

  def renderFrame(self, device, frameCount):
    count = frameCount % device.width
    oneline = [(0, 0, 0)] * (count) + [self.params['Color'].getRGBValues()] + [(0, 0, 0)] * (device.width - count - 1)
    im = Image.new('RGB', (device.width, device.height))
    im.putdata(oneline * device.height)
    return im
