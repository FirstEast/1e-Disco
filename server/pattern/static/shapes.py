from pattern.color import *
from pattern.pattern import *
from PIL import Image, ImageDraw

class Circle(StaticPattern):
  DEFAULT_PARAMS = {
    'Center X': 12,
    'Center Y': 12,
    'Radius': 10,
    'Fill': True,
    'Color': BLUE.getRGBValues()
  }

  def renderFrame(self, device):
    x0 = self.params['Center X']
    y0 = self.params['Center Y']
    r = self.params['Radius']
    
    im = Image.new('RGB', (device.width, device.height))
    draw = ImageDraw.Draw(im)
   
    if self.params['Fill']:
      draw.ellipse((x0 - r, y0 - r, x0 + r, y0 + r), outline=self.params['Color'], fill=self.params['Color'])    
    else:
      draw.ellipse((x0 - r, y0 - r, x0 + r, y0 + r), outline=self.params['Color'])    

    return im

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
