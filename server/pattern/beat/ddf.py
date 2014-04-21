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
    'Mirrored': True,
    'Flipped': False
  }

  USE_BEAT = True

  DEVICES = ['ddf']

  def render(self, device):
    freqs = BEAT_MODEL.avgFreqs
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
      if self.params['Flipped']:
        data += [self.params['Vis Color'].getRGBValues()] * smashed[i]
        data += [BLACK.getRGBValues()] * (device.width - smashed[i])
      else:
        data += [BLACK.getRGBValues()] * (device.width - smashed[i])
        data += [self.params['Vis Color'].getRGBValues()] * smashed[i]

    if self.params['Mirrored']:
      for i in range(len(smashed)-1, -1, -1):
        if self.params['Flipped']:
          data += [self.params['Vis Color'].getRGBValues()] * smashed[i]
          data += [BLACK.getRGBValues()] * (device.width - smashed[i])
        else:
          data += [BLACK.getRGBValues()] * (device.width - smashed[i])
          data += [self.params['Vis Color'].getRGBValues()] * smashed[i]

    frame.putdata(data)

    return frame

class HorizontalVis(Pattern):

  DEFAULT_PARAMS = {
    'Vis Color': RED,
    'Flipped': False
  }

  USE_BEAT = True

  DEVICES = ['ddf']

  def render(self, device):
    freqs = BEAT_MODEL.avgFreqs
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
      if self.params['Flipped']:
        row.reverse()
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

  def __init__(self, params):
    Pattern.__init__(self, params)
    self.lastTotal = 0

  def paramUpdate(self, paramName):
    self.circlePattern = loadSavedPatternFromFilename(self.params['Circle Pattern'])

  def render(self, device):
    total = getSummedFreqData(BEAT_MODEL, self.params['Frequency Band Start'], self.params['Frequency Band End'])
    thisTotal = total * SMOOTHING_ALPHA + self.lastTotal * (1 - SMOOTHING_ALPHA)
    self.lastTotal = total

    val = scaleToBucket(thisTotal, 1, self.params['Max Pulse'])
    self.circlePattern.setParam('Radius', val)
    return self.circlePattern.render(device)
