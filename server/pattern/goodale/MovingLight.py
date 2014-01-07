from pattern.color import *
from pattern.pattern import *

import time

class MovingLightPattern(Pattern):

  DEFAULT_PARAMS = {
    'color': Color([255, 0, 255]),
    'rate': 60
  }

  DEVICES = ['goodale']

  def __init__(self, beat, params):
    Pattern.__init__(self, beat, params);
    self.startTime = time.time() * 1000;

  def render(self, device):
    frameCount = int((time.time() * 1000 - self.startTime) / float(1000 / self.params['rate'])) % GOODALE_WIDTH
    frame = [[0, 0, 0]] * frameCount
    frame = frame + [self.params['color'].getRGBValues()]
    frame = frame + [[0, 0, 0]] * (GOODALE_WIDTH - 1 - frameCount)
    return [frame]