from pattern.color import *
from pattern.pattern import *

class Circle(StaticPattern):
  DEFAULT_PARAMS = {
    'Center X': 0,
    'Center Y': 0,
    'Radius': 10,
    'Fill': False,
    'Thickness': 1,
    'Color': BLUE
  }

  def renderFrame(self, device):
    x0 = self.params['Center X']
    y0 = self.params['Center Y']
    x = self.params['Radius']
    y = 0
    radiusError = 1 - x;
   
    frame = Frame([[BLACK] * device.width] * device.height)
    while x >= y:
      frame.drawPixel(x + x0, y + y0, self.params['Color'])
      frame.drawPixel(y + x0, x + y0, self.params['Color'])
      frame.drawPixel(-x + x0, y + y0, self.params['Color'])
      frame.drawPixel(-y + x0, x + y0, self.params['Color'])
      frame.drawPixel(-x + x0, -y + y0, self.params['Color'])
      frame.drawPixel(-y + x0, -x + y0, self.params['Color'])
      frame.drawPixel(x + x0, -y + y0, self.params['Color'])
      frame.drawPixel(y + x0, -x + y0, self.params['Color'])
      y += 1
      if radiusError < 0:
        radiusError+=2*y+1;
      else:
        x -= 1
        radiusError+=2*(y-x+1)
    return frame

class Rectangle(StaticPattern):
  DEFAULT_PARAMS = {
    'Origin X': 0,
    'Origin Y': 0,
    'Width': 10,
    'Height': 10,
    'Fill': False,
    'Thickness': 1,
    'Color': BLUE
  }
  pass

class Line(StaticPattern):
  DEFAULT_PARAMS = {
    'Point 1 X': 0,
    'Point 1 Y': 0,
    'Point 2 X': 0,
    'Point 2 Y': 0,
    'Thickness': 1,
    'Fill Above': False,
    'Fill Below': False,
    'Color': BLUE
  }
  pass

class Star(StaticPattern):
  DEFAULT_PARAMS = {
    'Center X': 0,
    'Center Y': 0,
    'Radius': 10,
    'Fill': False,
    'Color': BLUE
  }
  pass

class Heart(StaticPattern):
  DEFAULT_PARAMS = {
    'Center X': 0,
    'Center Y': 0,
    'Fill': False,
    'Color': RED
  }
  pass