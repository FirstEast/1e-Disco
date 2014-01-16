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
    vol = min(self.beat.volumes[0], 1.5)

    centroid = self.beat.centroids[0]
    centroidColor = getWeightedColorSum(self.params['color1'], self.params['color2'], centroid)
    emptyColor = centroidColor.getComplimentaryColor()

    pulse = int(vol * 100)
    sideFrame = [centroidColor] * pulse
    midFrame = [emptyColor] * (FLAT_GOODALE_LENGTH - pulse * 2)
    return unflattenGoodaleFrame(Frame([sideFrame + midFrame + sideFrame]))