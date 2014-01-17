from pattern.color import *
from pattern.pattern import *
from pattern.static.solid import *

class Adding(Pattern):
  def __init__(self, beat, params):
    Pattern.__init__(self, beat, params)
    self.p1 = SolidColor(beat, {})
    self.p2 = SolidColor(beat, {'Color': GREEN})
  
  def render(self, device):
    return self.p1.render(device) + self.p2.render(device)

class Subtracting(Pattern):
  def __init__(self, beat, params):
    Pattern.__init__(self, beat, params)
    self.p1 = SolidColor(beat, {'Color': WHITE})
    self.p2 = SolidColor(beat, {'Color': GREEN})
  
  def render(self, device):
    return self.p1.render(device) - self.p2.render(device)