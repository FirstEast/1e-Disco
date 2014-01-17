from pattern.color import *
from pattern.pattern import *
from pattern.util import *

from pattern.static.shapes import Circle

class PulsingCircle(Pattern):

  DEFAULT_PARAMS = {
    'Circle Color': BLUE,
    'Circle Fill': True,
    'Frequency Band Start': 0,
    'Frequency Band End': 8,
  }

  USE_BEAT = True

  DEVICES = ['ddf']

  def render(self, device):
    freqs = self.beat.frequencies[0]
    total = 0
    for i in range(self.params['Frequency Band Start'], self.params['Frequency Band End']):
      total += freqs[i]
    val = scaleToBucket(max(((total / (self.params['Frequency Band Start'] - self.params['Frequency Band End'])) - 0.66) * 3, 0), 0, device.height)

    circleParams = {
      'Center X': device.width / 2.0,
      'Center Y': device.height / 2.0,
      'Color': self.params['Circle Color'],
      'Fill': self.params['Circle Fill'],
      'Radius': val
    }
    circlePattern = Circle(self.beat, circleParams)
    return circlePattern.render()
