from pattern.color import *
from pattern.pattern import *

class MovingLinePattern(Pattern):

  DEFAULT_PARAMS = {
    'color': Color([255, 0, 0])
  }

  def __init__(self, beat, params):
    self.params = self.DEFAULT_PARAMS
    self.params.update(params)

    self.frameCount = 0

  def render(self, device):
    frame = [[[0, 0, 0]] * DDF_WIDTH] * DDF_HEIGHT
    for i in range(0, DDF_HEIGHT - 1):
      frame[i][self.frameCount] = self.params['color'].getRGBValues()

    self.frameCount += 1
    self.frameCount = self.frameCount % DDF_WIDTH
    return frame