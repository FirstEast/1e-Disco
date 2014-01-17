from pattern.color import *
from pattern.pattern import *
from pattern.util import *

class BeatTest(Pattern):

  DEFAULT_PARAMS = {
    'color1': RED,
    'color2': BLUE,
  }

  USE_BEAT = True

  DEVICES = ['goodale']

  def render(self, device):
    vol = min(self.beat.avgVolume, 1.0)

    centroid = self.beat.avgCentroid
    centroidColor = getWeightedColorSum(self.params['color1'], self.params['color2'], centroid)
    emptyColor = centroidColor.getComplimentaryColor()

    pulse = int(vol * FLAT_GOODALE_LENGTH/2.0)
    sideFrame = [centroidColor] * pulse
    midFrame = [emptyColor] * (FLAT_GOODALE_LENGTH - pulse * 2)
    return unflattenGoodaleFrame(Frame([sideFrame + midFrame + sideFrame]))