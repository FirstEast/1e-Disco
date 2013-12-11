from pattern.color import *
from pattern.Pattern import *
from pattern.ParameterTypes import *

class BeatTestPattern(Pattern):
  def __init__(self, params):
    self.expectedParams = {
      'color1': ParameterTypes.COLOR,
      'color2': ParameterTypes.COLOR,
      'beat': ParameterTypes.BEAT
    }
    self.defaultParams = {
      'color1': Color([1, 0, 0]),
      'color2': Color([0, 0, 255]),
      'beat': None
    }
    self.params = self.defaultParams
    self.params.update(params)

    self.frameCount = 0

  def getNextFrame(self):
    if self.params['beat'] == None:
      return [[0, 0, 0]] * Pattern.GOODALE_WIDTH

    leftVol = self.params['beat'].leftVolumes[0]
    rightVol = self.params['beat'].rightVolumes[0]

    centroid = (self.params['beat'].leftCentroids[0] + self.params['beat'].rightCentroids[0]) / 2.0
    centroidColor = getWeightedColorSum(self.params['color1'], self.params['color2'], centroid)

    leftPulse = int(leftVol * 100)
    rightPulse = int(rightVol * 100)
    leftFrame = [centroidColor.getRGBValues()] * leftPulse
    rightFrame = [centroidColor.getRGBValues()] * rightPulse
    midFrame = [[0, 0, 0]] * (Pattern.GOODALE_WIDTH - leftPulse - rightPulse)
    return leftFrame + midFrame + rightFrame