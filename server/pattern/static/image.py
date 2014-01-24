from pattern.color import *
from pattern.pattern import *
from pattern.mixer.layer import layerPatterns
from pattern.util import *

from PIL import Image

class AnimatedGif(TimedPattern):

  DEFAULT_PARAMS = {
    'Image Path': 'pattern/images/Pac Man DDF2.gif',
    'Resize': False,
    'DesWidth': 48,
    'DesHeight': 24,
    'RateMultiplier': 1.0
  }

  DEFAULT_PARAMS.update(TimedPattern.DEFAULT_PARAMS)

  DEVICES = ['ddf', 'goodale']

  def __init__(self, beat, params):
    TimedPattern.__init__(self, beat, params)
    self.oldCount = 0

  def paramUpdate(self):
    self.image = Image.open(self.params['Image Path'])
    self.params['Rate'] = float(1000 * self.params['RateMultiplier'] / self.image.info['duration'])
    self.frames = []
    lut = self.image.resize((256, 1))
    lut.putdata(range(256))
    pally = [el for lst in lut.convert("RGB").getdata() for el in lst]
    curFrame = self.image.copy()
    while True:
      curFrame.putpalette(pally)
      if self.params['Resize']:
        self.frames.append(curFrame.convert('RGB').resize((self.params['DesWidth'], self.params['DesHeight']), Image.NEAREST))
      else:
        self.frames.append(Image.new('RGB',self.image.size))
        self.frames[-1].paste(curFrame, (0, 0))
      try:
        self.image.seek(len(self.frames))
      except EOFError:
        break
      if len(self.frames) > 0 and self.image.dispose == None:
        curFrame = layerPatterns(self.image, curFrame,
          self.image.point(lambda x: int(x != self.image.info['transparency']) * 255, 'L'))
      else:
        curFrame = self.image.copy()

  def renderFrame(self, device, frameCount):
    frameCount %= len(self.frames)
    if device.name == 'goodale':
      im = Image.new('RGB', (DDF_WIDTH, DDF_HEIGHT))
      im.paste(self.frames[frameCount], (0, 0))
      return unflattenGoodaleArray(flatGoodaleArrayFromDdfImage(im))
    else:
      im = Image.new('RGB', (device.width, device.height))
      im.paste(self.frames[frameCount], (0, 0))
      return im

class AnimGif2(AnimatedGif):
  DEFAULT_PARAMS = {}
  DEFAULT_PARAMS.update(AnimatedGif.DEFAULT_PARAMS)
  DEFAULT_PARAMS.update({
    'Image Path': 'pattern/images/nyan.gif',
    'Resize': True
  })

class StaticImage(StaticPattern):
  DEFAULT_PARAMS = {
    'Image Path': 'pattern/images/1Emask.png'
  }

  def renderFrame(self, device):
    im = Image.open(self.params['Image Path'])
    im.convert('RGBA')
    im2 = Image.new('RGB', (device.width, device.height))

    im2.paste(im, (0,0))
    return im2
