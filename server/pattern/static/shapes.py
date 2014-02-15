from pattern.util import *
from pattern.color import *
from pattern.pattern import *
from PIL import Image, ImageDraw

class Circle(StaticPattern):
  DEFAULT_PARAMS = {
    'Center X': DDF_WIDTH / 2,
    'Center Y': DDF_HEIGHT / 2,
    'Radius': (DDF_HEIGHT / 2) - 2,
    'Fill': True,
    'Color': BLUE
  }

  def renderFrame(self, device):
    x0 = self.params['Center X']
    y0 = self.params['Center Y']
    r = self.params['Radius']
    
    im = Image.new('RGB', (device.width, device.height))
    draw = ImageDraw.Draw(im)
   
    if self.params['Fill']:
      draw.ellipse((x0 - r, y0 - r, x0 + r, y0 + r), outline=self.params['Color'].getRGBValues(), fill=self.params['Color'].getRGBValues())    
    else:
      draw.ellipse((x0 - r, y0 - r, x0 + r, y0 + r), outline=self.params['Color'].getRGBValues())    

    return im

class Rectangle(StaticPattern):
  DEFAULT_PARAMS = {
    'Origin X': 0,
    'Origin Y': 0,
    'Width': DDF_WIDTH - 1,
    'Height': DDF_HEIGHT - 1,
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
      draw.rectangle((x0, y0, x1, y1), outline=self.params['Color'].getRGBValues(), fill=self.params['Color'].getRGBValues())    
    else:
      draw.rectangle((x0, y0, x1, y1), outline=self.params['Color'].getRGBValues())    

    return im
