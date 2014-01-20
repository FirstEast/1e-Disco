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

class LotsOfCircles(Pattern):
  def __init__(self, beat, params):
    Pattern.__init__(self, beat, params)
    self.circle1 = PulsingCircle(beat, {'Circle Center X': 0, 'Circle Center Y': 0, 'Circle Color': BLUE})
    self.circle2 = PulsingCircle(beat, {'Circle Center X': 0, 'Circle Center Y': 24, 'Circle Color': RED})
    self.circle3 = PulsingCircle(beat, {'Circle Center X': 48, 'Circle Center Y': 0, 'Circle Color': RED})
    self.circle4 = PulsingCircle(beat, {'Circle Center X': 48, 'Circle Center Y': 24, 'Circle Color': BLUE})
    self.circle5 = PulsingCircle(beat, {'Circle Center X': 24, 'Circle Center Y': 0, 'Circle Color': GREEN, 'Max Pulse': 12})
    self.circle6 = PulsingCircle(beat, {'Circle Center X': 24, 'Circle Center Y': 24, 'Circle Color': GREEN, 'Max Pulse': 12})

  def render(self, device):
    pattern1 = self.circle1.render(device) 
    pattern2 = self.circle2.render(device)
    pattern3 = self.circle3.render(device)
    pattern4 = self.circle4.render(device)
    pattern5 = self.circle5.render(device)
    pattern6 = self.circle6.render(device)
    return ImageChops.add(ImageChops.add(ImageChops.add(pattern1, pattern2), ImageChops.add(pattern3, pattern4)), ImageChops.add(pattern5, pattern6))
