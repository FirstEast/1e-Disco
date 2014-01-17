from pattern.color import *
from pattern.pattern import *
from pattern.util import *

from pattern.static.shapes import Circle

from PIL import Image

BASS = (0, 8)

SMOOTHING_ALPHA = 0.7

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

    if self.params['Mirrored']:
      div = 4
    else:
      div = 2

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

    frame = []
    for i in range(len(freqs)):
      row = []
      for j in range(device.height - newFreqs[i]):
        row.append(BLACK.getRGBValues())
      for j in range(newFreqs[i]):
        row.append(self.params['Vis Color'].getRGBValues())
      frame += row
    im = Image.new('RGB', (device.height, len(freqs)))
    im.putdata(frame)
    return im.transpose(Image.ROTATE_270).transpose(Image.FLIP_LEFT_RIGHT)

class PulsingCircle(Pattern):

  DEFAULT_PARAMS = {
    'Circle Color': BLUE,
    'Circle Fill': True,
    'Frequency Band Start': BASS[0],
    'Frequency Band End': BASS[1],
  }

  USE_BEAT = True

  DEVICES = ['ddf']

  def __init__(self, beat, params):
    Pattern.__init__(self, beat, params)
    self.lastTotal = 0

  def render(self, device):
    freqs = self.beat.avgFreqs
    total = 0
    for i in range(self.params['Frequency Band Start'], self.params['Frequency Band End']):
      total += (freqs[i] - 0.80) * 5
    thisTotal = total * SMOOTHING_ALPHA + self.lastTotal * (1 - SMOOTHING_ALPHA)
    self.lastTotal = total

    val = scaleToBucket(thisTotal / (self.params['Frequency Band End'] - self.params['Frequency Band Start']), 0, device.height)
    circleParams = {
      'Center X': device.width / 2.0,
      'Center Y': device.height / 2.0,
      'Color': self.params['Circle Color'].getRGBValues(),
      'Fill': self.params['Circle Fill'],
      'Radius': val
    }
    circlePattern = Circle(self.beat, circleParams)

    return circlePattern.render(device)
