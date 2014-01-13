from pattern.color import *
from pattern.pattern import *

class BeatTestPattern(Pattern):

  DEFAULT_PARAMS = {
    'color1': Color([255, 0, 0]),
    'color2': Color([0, 0, 255]),
  }

  USE_BEAT = True

  DEVICES = ['goodale']

  def render(self, device):
    leftVol = min(self.beat.leftVolumes[0], 1.5)
    rightVol = min(self.beat.rightVolumes[0], 1.5)

    centroid = (self.beat.leftCentroids[0] + self.beat.rightCentroids[0]) / 2.0
    centroidColor = getWeightedColorSum(self.params['color1'], self.params['color2'], centroid)

    leftPulse = int(leftVol * 100)
    rightPulse = int(rightVol * 100)
    leftFrame = [centroidColor.getRGBValues()] * leftPulse
    rightFrame = [centroidColor.getRGBValues()] * rightPulse
    midFrame = [[0, 0, 0]] * (GOODALE_WIDTH - leftPulse - rightPulse)
    return [leftFrame + midFrame + rightFrame]