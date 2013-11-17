from pattern.Color import *
from pattern.Pattern import *
from pattern.ParameterTypes import *

class MovingLinePattern(Pattern):
  def __init__(self, params):
    self.expectedParams = {
      'color': ParameterTypes.COLOR
    }
    self.defaultParams = {
      'color': Color([255, 0, 0])
    }
    self.params = self.defaultParams
    self.params.update(params)

    self.frameCount = 0

  def getNextFrame(self):
    frame = [[[0, 0, 0]] * Pattern.DDF_WIDTH] * Pattern.DDF_HEIGHT
    for i in range(0, Pattern.DDF_HEIGHT - 1):
      frame[i][self.frameCount] = self.params['color'].getRGBValues()

    self.frameCount += 1
    self.frameCount = self.frameCount % Pattern.DDF_WIDTH
    return frame