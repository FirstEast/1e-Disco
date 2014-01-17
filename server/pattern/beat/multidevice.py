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

    frame = []
    for i in range(len(smashed)):
      row = []
      for j in range(device.width - smashed[i]):
        row.append(BLACK)
      for j in range(smashed[i]):
        row.append(self.params['Vis Color'])
      frame.append(row)

    return Frame(frame)

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
      frame.append(row)

    return Frame(frame).transpose()
