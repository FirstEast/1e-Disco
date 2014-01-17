from pattern.color import *
from pattern.pattern import *
from pattern.util import *

from goodale import *

class VerticalVis(Pattern):

  DEFAULT_PARAMS = {
    'Vis Color': RED,
  }

  USE_BEAT = True

  DEVICES = ['goodale', 'ddf']

  def __init__(self, beat, params):
    Pattern.__init__(self, beat, params)

    self.goodalePattern = BeatTest(beat, {})

  def render(self, device):
    if device.name == 'ddf':
      return self.renderDdf(device)
    elif device.name == 'goodale':
      return self.goodalePattern.render()

  def renderDdf(self, device):
    freqs = self.beat.frequencies[0]
    smashed = []
    for i in range(int(len(freqs) / 2.0)):
      val = scaleToBucket(max((((freqs[2*i] + freqs[2*i + 1]) / 2.0) - 0.66) * 3, 0), 0, device.width)
      smashed.append(val)

    frame = Image.new('RGB', (device.width, len(smashed)))
    data = []

    for i in range(len(smashed)):
      data += [BLACK.getRGBValues()] * (device.width - smashed[i])
      data += [self.params['Vis Color'].getRGBValues()] * smashed[i]

    frame.putdata(data)

    return frame

class HorizontalVis(Pattern):

  DEFAULT_PARAMS = {
    'Vis Color': RED,
  }

  USE_BEAT = True

  DEVICES = ['goodale', 'ddf']

  def __init__(self, beat, params):
    Pattern.__init__(self, beat, params)

    self.goodalePattern = BeatTest(beat, {})

  def render(self, device):
    if device.name == 'ddf':
      return self.renderDdf(device)
    elif device.name == 'goodale':
      return self.goodalePattern.render()

  def renderDdf(self, device):
    freqs = self.beat.frequencies[0]
    newFreqs = []
    for i in range(len(freqs)):
      newFreqs.append(scaleToBucket(max((freqs[i] - 0.66) * 3, 0), 0, device.height))

    frame = []
    for i in range(len(freqs)):
      row = []
      for j in range(device.height - newFreqs[i]):
        row.append(BLACK)
      for j in range(newFreqs[i]):
        row.append(self.params['Vis Color'])
      frame += row
    im = Image.new('RGB', (device.height, len(freqs)))
    im.putdata(frame)
    return im.transpose(ROTATE_270).transpose(FLIP_LEFT_RIGHT)


