from pattern.pattern import *
from pattern.color import *

class BemisMovingLightPattern(Pattern):

  DEFAULT_PARAMS = {
    'color': Color([255, 0, 255])
  }

  DEVICES = ['bemis']

  def __init__(self, beat, params):
    self.params = self.DEFAULT_PARAMS
    self.params.update(params)

    self.frameCount = 0

  def render(self, device):
    frame = [[0, 0, 0]] * self.frameCount
    frame = frame + [self.params['color'].getRGBValues()]
    frame = frame + [[0, 0, 0]] * (BEMIS_WIDTH - 1 - self.frameCount)
    self.frameCount += 1
    self.frameCount = self.frameCount % BEMIS_WIDTH
    return [frame]