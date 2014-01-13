from pattern.color import *
from pattern.pattern import *
import time

class MovingLinePattern(Pattern):

  DEFAULT_PARAMS = {
    'color': Color([255, 0, 0]),
    'rate': 60
  }

  DEVICES = ['ddf']

  def __init__(self, beat, params):
    Pattern.__init__(self, beat, params)
    self.startTime = time.time() * 1000

  def render(self, device):
    frameCount = int((time.time() * 1000 - self.startTime) / float(1000 / self.params['rate'])) % DDF_WIDTH
    frame = [[[0, 0, 0]] * DDF_WIDTH] * DDF_HEIGHT
    for i in range(0, DDF_HEIGHT - 1):
      frame[i][frameCount] = self.params['color']
    return frame