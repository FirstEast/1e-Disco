# The colorsys module offers rgb/hsv conversion utilities, 
# so I didn't do it here.

import colorsys

def interpolateColors(color1, color2):
  diffs = []
  for i in range(len(color1.getRGBValues())):
    diffs.append(color2[i] - color1[i])
  max_diff = max([abs(i) for i in diffs])

  result = []
  for i in range(max_diff):
    scale = float(i) / max_diff
    next = Color([color1[0] + diffs[0]*scale, color1[1] + diffs[1]*scale, color1[2] + diffs[2]*scale])
    result.append(next)
  result.append(color2)
  return result

def getWeightedColorSum(color1, color2, split):
  return color1 * split + color2 * (1-split)

def clampRGB(RGBValues):
  red = int(min(max(0, RGBValues[0]), 255))
  green = int(min(max(0, RGBValues[1]), 255))
  blue = int(min(max(0, RGBValues[2]), 255))
  return (red, green, blue)

def HSV_shift(colvals, dh, ds, dv):
  rgb = [val/255.0 for val in colvals]
  hsv = colorsys.rgb_to_hsv(*rgb)
  hsv = [hsv[0] + dh, hsv[1] + ds * hsv[1], hsv[2] + dv * hsv[2]]
  rgb = colorsys.hsv_to_rgb(*hsv)
  return clampRGB([int(val*255) for val in rgb])

class Color():
  """
  Color class. Contains operator and other utilities for manipulating colors in patterns.

  Contains a list of 3 values (red, green, and blue)
  """

  def __init__(self, RGBValues):
    self.RGBValues = clampRGB(RGBValues)

  def __init__(self, values, isHSV = False):
    if (isHSV): 
      rgb = colorsys.hsv_to_rgb(*values)
    else:
      rgb = values
    self.RGBValues = clampRGB(rgb)

  def getRGBValues(self):
    return self.RGBValues

  def setRGBValues(self, RGBValues):
    self.RGBValues = RGBValues

  def getComplimentaryColor(self):
    """
    Returns color with opposite RGB.  For example, if RGB is (12,13,14), 
    then this returns (243, 242, 241)
    """
    red = 255 - self.RGBValues[0]
    green = 255 - self.RGBValues[1]
    blue = 255 - self.RGBValues[2]
    return Color(clampRGB([red, green, blue]))

  def darken(self, percent):
    """
    Darkens color by scaling down magnitudes.
    """
    scalar = 1.0 - percent
    self = self * scalar

  def lighten(self, percent):
    """
    Lightens color by scaling up magnitudes.
    """
    scalar = 1.0 + percent
    self = self * scalar

  def saturate(self, percent):
    rgb = [val/255.0 for val in self.RGBValues]
    hsv = colorsys.rgb_to_hsv(*rgb)
    hsv = [hsv[0], hsv[1] + percent*hsv[1], hsv[2]]
    rgb = colorsys.hsv_to_rgb(*hsv)
    return clampRGB([int(val*255) for val in rgb])

  def desaturate(self, percent):
    rgb = [val/255.0 for val in self.RGBValues]
    hsv = colorsys.rgb_to_hsv(*rgb)
    hsv = [hsv[0], hsv[1] - percent*hsv[1], hsv[2]]
    rgb = colorsys.hsv_to_rgb(*hsv)
    return clampRGB([int(val*255) for val in rgb])

  def __add__(self, color):
    if isinstance(color, Color):
      red = self.RGBValues[0] + color.getRGBValues()[0]
      green = self.RGBValues[1] + color.getRGBValues()[1]
      blue = self.RGBValues[2] + color.getRGBValues()[2]
      return Color(clampRGB([red, green, blue]))
    else:
      raise TypeError

  def __sub__(self, color):
    if isinstance(color, Color):
      red = self.RGBValues[0] - color.getRGBValues()[0]
      green = self.RGBValues[1] - color.getRGBValues()[1]
      blue = self.RGBValues[2] - color.getRGBValues()[2]
      return Color(clampRGB([red, green, blue]))
    else:
      raise TypeError

  def __mul__(self, scalar):
    if type(scalar) is int or type(scalar) is float:
      red = self.RGBValues[0] * scalar
      green = self.RGBValues[1] * scalar
      blue = self.RGBValues[2] * scalar
      return Color(clampRGB([red, green, blue]))
    else:
      raise TypeError

  def __div__(self, scalar):
    if type(scalar) is int or type(scalar) is float:
      red = self.RGBValues[0] / float(scalar)
      green = self.RGBValues[1] / float(scalar)
      blue = self.RGBValues[2] / float(scalar)
      return Color(clampRGB([red, green, blue]))
    else:
      raise TypeError

  def __getitem__(self, k):
    return self.RGBValues[k]

  def __eq__(self, other):
    if type(other) is type(self):
      return self.__dict__ == other.__dict__
    return False

  def __str__(self):
    return 'RGB Values: ' + str(self.RGBValues)

# Color constants
BLACK = Color([0,0,0])
WHITE = Color([255,255,255])
RED = Color([255,0,0])
GREEN = Color([0,255,0])
BLUE = Color([0,0,255])
