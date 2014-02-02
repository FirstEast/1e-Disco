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
    draw.text(((device.height / 6) - 1, (device.width / 6) - 1), self.params['String'], fill=self.params['Color'].getRGBValues())
    return im
