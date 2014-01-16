from pattern.color import *
from pattern.pattern import *
import time

class Interpolation(Pattern):

  DEFAULT_PARAMS = {
    'Colors': [RED, GREEN, BLUE],
    'rate': 120
  }

  DEVICES = ['goodale', 'bemis']

  def __init__(self, beat, params):
    Pattern.__init__(self, beat, params)
    self.startTime = time.time() * 1000

  def paramUpdate(self):
    self.loop = []
    colors = self.params['Colors'] + [self.params['Colors'][0]]
    for i in range(len(self.params['Colors'])):
      self.loop += interpolateColors(colors[i], colors[i+1])

  def render(self, device):
    frameCount = int((time.time() * 1000 - self.startTime) / float(1000 / self.params['rate'])) % len(self.loop)
    frame = [self.loop[frameCount]] * device.width
    return [frame]