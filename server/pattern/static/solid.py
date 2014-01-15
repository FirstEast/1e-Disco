from pattern.color import *
from pattern.pattern import *

# IMPORTANT
# Static patterns should render ONCE then cache their answer.
# There's no point in recalculating unless your parameters change.

class SolidColor(Pattern):
  pass

class Gradient(Pattern):
  # Radial, linear, multicolor.
  # interpolateColors function can help you do this
  # Also make a parameter a color list so you can have N color gradients
  pass