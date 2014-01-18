from pattern.color import *
from pattern.pattern import *
from PIL import Image, ImageDraw

class Circle(StaticPattern):
  DEFAULT_PARAMS = {
    'Center X': 24,
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
    'Color': BLUE
  }
  
  def renderFrame(self, device):
    x0 = self.params['Origin X']
    y0 = self.params['Origin Y']
    x1 = x0 + self.params['Width']
    y1 = y0 + self.params['Height']
    
    im = Image.new('RGB', (device.width, device.height))
    draw = ImageDraw.Draw(im)
   
    if self.params['Fill']:
      draw.rectangle((x0, y0, x1, y), outline=self.params['Color'], fill=self.params['Color'])    
    else:
      draw.rectangle((x0, y0, x1, y1), outline=self.params['Color'])    

    return im

class Line(StaticPattern):
  DEFAULT_PARAMS = {
    'Point 1 X': 12,
    'Point 1 Y': 6,
    'Point 2 X': 36,
    'Point 2 Y': 18,
    'Thickness': 1,
    'Fill Above': False,
    'Fill Below': False,
    'Color': RED
  }
  
  def renderFrame(self, device):
    x0 = self.params['Point 1 X']
    y0 = self.params['Point 1 Y']
    x1 = self.params['Point 2 X']
    y1 = self.params['Point 2 Y']

    im = Image.new('RGB', (device.width, device.height))
    draw = ImageDraw.Draw(im)

    draw.line([(x0, y0), (x1, y1)], fill=self.params['Color'].getRGBValues(), width=self.params['Thickness'])

    return im

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
