# The colorsys module offers rgb/hsv conversion utilities, 
# so I didn't do it here.

import colorsys

def interpolateColors(color1, color2):
  pass

def clampRGB(RGBValues):
  red = min(max(0, RGBValues[0]), 255)
  green = min(max(0, RGBValues[1]), 255)
  blue = min(max(0, RGBValues[2]), 255)
  return [red, green, blue]

class Color():
  def __init__(self, RGBValues):
    self.RGBValues = RGBValues

  def getRGBValues(self):
    return self.RGBValues

  def setRGBValues(self, RGBValues):
    self.RGBValues = RGBValues

  def getComplimentaryColor(self):
    pass

  def darken(self, percent):
    pass

  def lighten(self, percent):
    pass

  def saturate(self, percent):
    rgb = [val/255.0 for val in self.RGBValues]
    hsv = colorsys.rgb_to_hsv(*rgb)
    hsv = [hsv[0], hsv[1] + percent*hsv[1], hsv[2]]
    rgb = colorsys.hsv_to_rgb(*hsv)
    return clamp([int(val*255) for val in rgb])

  def desaturate(self, percent):
    rgb = [val/255.0 for val in self.RGBValues]
    hsv = colorsys.rgb_to_hsv(*rgb)
    hsv = [hsv[0], hsv[1] - percent*hsv[1], hsv[2]]
    rgb = colorsys.hsv_to_rgb(*hsv)
    return clampRGB([int(val*255) for val in rgb])

  def addColor(self, color):
    red = self.RGBValues[0] + color[0]
    green = self.RGBValues[1] + color[1]
    blue = self.RGBValues[2] + color[2]
    return clampRGB([red, green, blue])

  def subtractColor(self, color):
    red = self.RGBValues[0] - color[0]
    green = self.RGBValues[1] - color[1]
    blue = self.RGBValues[2] - color[2]
    return clampRGB([red, green, blue])