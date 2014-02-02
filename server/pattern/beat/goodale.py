from pattern.color import *
from pattern.pattern import *
from pattern.util import *

class VolumePulse(Pattern):

  DEFAULT_PARAMS = {
    'Pulse Color 1': RED,
    'Pulse Color 2': BLUE,
  }

  USE_BEAT = True

  DEVICES = ['goodale']

  def render(self, device):
    vol = min(self.beat.avgVolume, 1.0)

    centroid = self.beat.avgCentroid
    centroidColor = getWeightedColorSum(self.params['Pulse Color 1'], self.params['Pulse Color 2'], centroid)
    emptyColor = centroidColor.getComplimentaryColor().getRGBValues()
    centroidColor = centroidColor.getRGBValues()

    pulse = int(vol * FLAT_GOODALE_LENGTH/2.0)
    sideFrame = [centroidColor] * pulse
    midFrame = [emptyColor] * (FLAT_GOODALE_LENGTH - pulse * 2)
    return unflattenGoodaleArray([sideFrame + midFrame + sideFrame])