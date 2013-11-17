from pattern.color import *
from pattern.Pattern import *
from pattern.ParameterTypes import *

class MovingLightPattern(Pattern):
  def __init__(self, params):
    self.expectedParams = {
      'color': ParameterTypes.COLOR
    }
    self.defaultParams = {
      'color': Color([255, 0, 255])
    }
    self.params = self.defaultParams
    self.params.update(params)

    self.frameCount = 0

  def getNextFrame(self):
    frame = [0, 0, 0] * self.frameCount
    frame = frame + self.params['color'].getRGBValues()
    frame = frame + [0, 0, 0] * (Pattern.GOODALE_WIDTH - 1 - self.frameCount)
    self.frameCount += 1
    self.frameCount = self.frameCount % Pattern.GOODALE_WIDTH
    return frame