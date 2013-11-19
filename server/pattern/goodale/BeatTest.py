from pattern.color import *
from pattern.Pattern import *
from pattern.ParameterTypes import *

class BeatTestPattern(Pattern):
  def __init__(self, params):
    self.expectedParams = {
      'color': ParameterTypes.COLOR,
      'beat': ParameterTypes.BEAT
    }
    self.defaultParams = {
      'color': Color([255, 0, 255]),
      'beat': None
    }
    self.params = self.defaultParams
    self.params.update(params)

    self.frameCount = 0

  def getNextFrame(self):
    if self.params['beat'] == None:
      return [0, 0, 0] * Pattern.GOODALE_WIDTH

    leftVol = self.params['beat'].leftVolumes[0]
    rightVol = self.params['beat'].rightVolumes[0]

    leftPulse = int(leftVol * 100)
    rightPulse = int(rightVol * 100)
    leftFrame = self.params['color'].getRGBValues() * leftPulse
    rightFrame = self.params['color'].getRGBValues() * rightPulse
    midFrame = [0, 0, 0] * (Pattern.GOODALE_WIDTH - leftPulse - rightPulse)
    return leftFrame + midFrame + rightFrame