from pattern.color import *
from pattern.pattern import *
import time

class Interpolation(Pattern):

  DEFAULT_PARAMS = {
    'color 1': Color([255, 0, 0]),
    'color 2': Color([0, 255, 0]),
    'color 3': Color([0, 0, 255]),
    'rate': 120
  }

  DEVICES = ['goodale', 'bemis']

  def __init__(self, beat, params):
    Pattern.__init__(self, beat, params)
    self.startTime = time.time() * 1000

    loop1 = interpolateColors(self.params['color 1'], self.params['color 2'])
    loop2 = interpolateColors(self.params['color 2'], self.params['color 3'])
    loop3 = interpolateColors(self.params['color 3'], self.params['color 1'])
    self.loop = loop1 + loop2 + loop3

  def render(self, device):
    frameCount = int((time.time() * 1000 - self.startTime) / float(1000 / self.params['rate'])) % len(self.loop)
    frame = [self.loop[frameCount]] * device.width
    return [frame]