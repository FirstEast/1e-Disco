from pattern.color import *
from pattern.pattern import *
from pattern.static.solid import *
from pattern.beat.ddf import *
from pattern.mixer.layer import *
from PIL import Image, ImageChops

class MaskingBeats(Pattern):
  def __init__(self, beat, params):
    Pattern.__init__(self, beat, params)
    self.circle = PulsingCircle(beat, {})
    self.vis = VerticalVis(beat, {})

  def render(self, device):
    circlePattern = self.circle.render(device)
    visPattern = self.vis.render(device)
    maskedVisPattern = maskPatterns(circlePattern, visPattern)
    return ImageChops.add(circlePattern, maskedVisPattern)

class DoubleVis(Pattern):
  def __init__(self, beat, params):
    Pattern.__init__(self, beat, params)
    self.vis1 = VerticalVis(beat, {'Vis Color': BLUE})
    self.vis2 = VerticalVis(beat, {})

  def render(self, device):
    visPattern1 = self.vis1.render(device)
    visPattern2 = self.vis2.render(device)
    return ImageChops.add(visPattern1, visPattern2.transpose(Image.FLIP_LEFT_RIGHT))
