from pattern.color import *
from pattern.pattern import *
from PIL import Image,ImageDraw

# class Letter(StaticPattern):
#   pass

class Word(StaticPattern):
  DEFAULT_PARAMS = {
    'String': 'HELLO',
    'Color': BLUE
  }
  
  def renderFrame(self, device):
    im = Image.new('RGB', (device.width, device.height))
    draw = ImageDraw.Draw(im)
    print draw.textsize(self.params['String'])
    draw.text((3, 7), self.params['String'], fill=self.params['Color'].getRGBValues())
    return im
