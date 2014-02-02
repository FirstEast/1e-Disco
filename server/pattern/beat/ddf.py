from pattern.color import *
from pattern.pattern import *
from pattern.util import *
from pattern.mixer.layer import *
from pattern.importer import *

from pattern.static.shapes import Circle
from pattern.static.solid import *

from PIL import Image, ImageChops, ImageEnhance

SMOOTHING_ALPHA = 0.8

class VerticalVis(Pattern):

  DEFAULT_PARAMS = {
    'Vis Color': RED,
    'Mirrored': True
  }

  USE_BEAT = True

  DEVICES = ['ddf']

  def render(self, device):
    freqs = self.beat.avgFreqs
    smashed = []

    div = len(freqs) / device.height
    if self.params['Mirrored']:
      div = div * 2

    for i in range(int(len(freqs) / div)):
      total = 0
      for j in range(0, int(div)):
        total += freqs[div*i + j]
      val = scaleToBucket(max(((total / div) - 0.75) * 4, 0), 0, device.width)
      smashed.append(val)

    smashed.reverse() # We want the bass inside!
    frame = Image.new('RGB', (device.width, len(smashed) * (div/2)))
    data = []

    for i in range(len(smashed)):
      data += [BLACK.getRGBValues()] * (device.width - smashed[i])
      data += [self.params['Vis Color'].getRGBValues()] * smashed[i]

    if self.params['Mirrored']:
      for i in range(len(smashed)-1, -1, -1):
        data += [BLACK.getRGBValues()] * (device.width - smashed[i])
        data += [self.params['Vis Color'].getRGBValues()] * smashed[i]

    frame.putdata(data)

    return frame

class HorizontalVis(Pattern):

  DEFAULT_PARAMS = {
    'Vis Color': RED,
  }

  USE_BEAT = True

  DEVICES = ['ddf']

  def render(self, device):
    freqs = self.beat.avgFreqs
    newFreqs = []
    for i in range(len(freqs)):
      newFreqs.append(scaleToBucket(max((freqs[i] - 0.66) * 3, 0), 0, device.height))

    mergedFreqs = []
    bucketsPerRow = len(newFreqs) / device.width
    for i in range(device.width):
      index = i * bucketsPerRow
      total = 0
      for j in range(bucketsPerRow):
        total += newFreqs[index + j]
      mergedFreqs.append(total / bucketsPerRow)

    frame = []
    for i in range(len(mergedFreqs)):
      row = []
      for j in range(device.height - mergedFreqs[i]):
        row.append(BLACK.getRGBValues())
      for j in range(mergedFreqs[i]):
        row.append(self.params['Vis Color'].getRGBValues())
      frame += row
    im = Image.new('RGB', (device.height, len(mergedFreqs)))
    im.putdata(frame)
    return im.transpose(Image.ROTATE_270).transpose(Image.FLIP_LEFT_RIGHT)

class PulsingCircle(Pattern):

  DEFAULT_PARAMS = {
    'Circle Pattern': 'default_circle.json',
    'Max Pulse': DDF_HEIGHT,
    'Frequency Band Start': BASS[0],
    'Frequency Band End': BASS[1]
  }

  USE_BEAT = True

  DEVICES = ['ddf']

  def __init__(self, beat, params):
    Pattern.__init__(self, beat, params)
    self.lastTotal = 0

  def paramUpdate(self, paramName):
    self.circlePattern = loadSavedPatternFromFilename(self.beat, self.params['Circle Pattern'])

  def render(self, device):
    total = getSummedFreqData(self.beat, self.params['Frequency Band Start'], self.params['Frequency Band End'])
    thisTotal = total * SMOOTHING_ALPHA + self.lastTotal * (1 - SMOOTHING_ALPHA)
    self.lastTotal = total

    val = scaleToBucket(thisTotal, 1, self.params['Max Pulse'])
    self.circlePattern.setParam('Radius', val)
    return self.circlePattern.render(device)

class FadingPulsingCircle(Pattern):
  DEFAULT_PARAMS = {
    'Pulsing Circle Pattern': 'default_pulsingCircle.json',
  }

  USE_BEAT = True

  DEVICES = ['ddf']

  def paramUpdate(self, paramName):
    self.circlePattern = loadSavedPatternFromFilename(self.beat, self.params['Pulsing Circle Pattern'])    

  def render(self, device):
    total = getSummedFreqData(self.beat, self.circlePattern.params['Frequency Band Start'], self.circlePattern.params['Frequency Band End'])
    pattern = self.circlePattern.render(device)
    enhancer = ImageEnhance.Brightness(pattern)
    pattern = enhancer.enhance(total)

    return pattern

class ColorPulsingCircle(Pattern):
  DEFAULT_PARAMS = {
    'Pulsing Circle Pattern': 'default_pulsingCircle.json',
    '100Start Hue': 25,
    '100End Hue': 75
  }

  USE_BEAT = True

  DEVICES = ['ddf']

  def paramUpdate(self, paramName):
    self.circlePattern = loadSavedPatternFromFilename(self.beat, self.params['Pulsing Circle Pattern'])    

  def render(self, device):
    cent = max(self.beat.avgCentroid - 0.66, 0) * 3
    hue = (self.params['100End Hue'] - self.params['100Start Hue']) * cent + self.params['100Start Hue']
    circleColor = Color((hue / 100.0, 1, 255), isHSV=True)
    solidColorPattern = SolidColor(self.beat, {'Color': circleColor})

    return maskPatterns(self.circlePattern.render(device), solidColorPattern.render(device))
