from pattern.color import *
from pattern.pattern import *

from PIL import Image

class StaticImage(StaticPattern):
  DEFAULT_PARAMS = {
    'Image Path': 'pattern/images/StarSprite.png'
  }

  def renderFrame(self, device):
    im = Image.open(self.params['Image Path'])
    im.convert('RGBA')
    im2 = Image.new('RGB', (device.width, device.height))

    im2.paste(im, (0,0))
    return im2