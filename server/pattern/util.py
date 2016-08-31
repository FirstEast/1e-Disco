from pattern import *
from model.inputs import BeatModel, KeyModel

from PIL import Image

import math

# Device constants
GOODALE_WIDTH = 395
GOODALE_HEIGHT = 1
GOODALE_FORMAT = 'BGR'

DEMO_MODULE = False
if DEMO_MODULE:
  DDF_WIDTH = 16
  DDF_HEIGHT = 12
else:
  DDF_WIDTH = 48
  DDF_HEIGHT = 24

BEMIS_WIDTH = 264
BEMIS_HEIGHT = 1
BEMIS_FORMAT = 'GRB'

FLAT_GOODALE_TOP = 160
FLAT_GOODALE_SIDE = 97
FLAT_GOODALE_BOTTOM = 159
FLAT_GOODALE_LENGTH = FLAT_GOODALE_TOP + FLAT_GOODALE_SIDE + FLAT_GOODALE_BOTTOM

# Frequency band constants
BASS = (0, 8)

# Global input models
BEAT_MODEL = BeatModel()
KEY_MODEL = KeyModel()

def unflattenGoodaleArray(frame):
  newFrame = []
  for i in range(len(frame[0])):
    if i > 161 and i < 208:
      continue
    elif i == 270:
      for j in range(13):
        newFrame.append(frame[0][i])
    elif i == 401:
      for j in range(14):
        newFrame.append(frame[0][i])
    else:
      newFrame.append(frame[0][i])
  im = Image.new('RGB', (len(newFrame), 1))
  im.putdata(newFrame)
  return im

def flatGoodaleArrayFromDdfImage(ddfImage):
  (width, height) = ddfImage.size
  data = ddfImage.getdata()
  pxPerWidth = FLAT_GOODALE_TOP / width
  pxPerHeight = FLAT_GOODALE_SIDE / height

  top = []
  side = []
  bottom = []
  for i in range(0, width):
    top += pxPerWidth * [data[i]]
    bottom += pxPerWidth * [(data[(height-1)*(width) + i])]
  for i in range(0, height):
    side += pxPerHeight * [data[width*i]]
  bottom += [(0,0,0)] * (FLAT_GOODALE_BOTTOM - len(bottom))
  bottom.reverse()
  side.reverse()
  top += [(0,0,0)] * (FLAT_GOODALE_TOP - len(top))
  side += [(0,0,0)] * (FLAT_GOODALE_SIDE - len(side))
  return [bottom + side + top]

def scaleToBucket(value, minVal, maxVal):
  v = min(max(value, 0.0), 1.0)
  v = (maxVal - minVal) * value + minVal
  v = min(max(v, minVal), maxVal)
  return int(math.floor(v))

def getSummedFreqData(beat, start, end):
  freqs = beat.avgFreqs
  total = 0
  for i in range(start, end):
    total += (freqs[i] - 0.80) * 5
  return total / (end - start)

def layerPatterns(top, bottom, mask = -1, flip = True, blend = False): # by default, mask's black is the bottom layer
  if mask == -1: mask = top
  topData = top.getdata()
  maskData = mask.convert('L').getdata()
  botData = bottom.getdata()

  newData = []
  for i in range(len(maskData)):
    if (maskData[i] > 0) != flip:
      newData.append(botData[i])
    else:
      newData.append(topData[i])
  ret = bottom.copy()
  ret.putdata(newData)
  return ret

def maskPatterns(mask, patternImg): # mask's light is what to keep
  mask = mask.convert('L')
  return layerPatterns(mask, patternImg, mask, False)

KEY_COLOR_MAPPING_1 = {
  'q': Color((25, 0, 0)),
  'w': Color((50, 0, 0)),
  'e': Color((75, 0, 0)),
  'r': Color((100, 0, 0)),
  't': Color((125, 0, 0)),
  'y': Color((150, 0, 0)),
  'u': Color((175, 0, 0)),
  'i': Color((200, 0, 0)),
  'o': Color((225, 0, 0)),
  'p': Color((250, 0, 0)),
  '[': Color((255, 0, 0)),
  ']': Color((255, 0, 0)),
  'a': Color((0, 25, 0)),
  's': Color((0, 50, 0)),
  'd': Color((0, 75, 0)),
  'f': Color((0, 100, 0)),
  'g': Color((0, 125, 0)),
  'h': Color((0, 150, 0)),
  'j': Color((0, 175, 0)),
  'k': Color((0, 200, 0)),
  'l': Color((0, 225, 0)),
  ';': Color((0, 250, 0)),
  "'": Color((0, 255, 0)),
  'z': Color((0, 0, 25)),
  'x': Color((0, 0, 50)),
  'c': Color((0, 0, 75)),
  'v': Color((0, 0, 100)),
  'b': Color((0, 0, 125)),
  'n': Color((0, 0, 150)),
  'm': Color((0, 0, 175)),
  ',': Color((0, 0, 200)),
  '.': Color((0, 0, 225)),
  '/': Color((0, 0, 250)),
  'up': Color((0, 0, 0)),
  'down': Color((0, 0, 0)),
  'left': Color((0, 0, 0)),
  'right': Color((0, 0, 0)),
  'tab': Color((0, 0, 0)),
  'enter': Color((0, 0, 0)),
  'del': Color((0, 0, 0)),
  'backspace': Color((0, 0, 0)),
  'space': Color((255, 255, 255)),
}

KEY_COLOR_MAPPING_2 = {
  'q': Color((255, 0, 0)),
  'w': Color((0, 255, 0)),
  'e': Color((0, 0, 255)),
  'r': Color((255, 255, 0)),
  't': Color((255, 0, 255)),
  'y': Color((0, 255, 255)),
  'u': Color((127,255,0)),
  'i': Color((220,20,60)),
  'o': Color((255,140,0)),
  'p': Color((255,20,147)),
  '[': Color((0, 0, 0)),
  ']': Color((0, 0, 0)),
  'a': Color((255, 0, 0)) * 0.66,
  's': Color((0, 255, 0)) * 0.66,
  'd': Color((0, 0, 255)) * 0.66,
  'f': Color((255, 255, 0)) * 0.66,
  'g': Color((255, 0, 255)) * 0.66,
  'h': Color((0, 255, 255)) * 0.66,
  'j': Color((127,255,0)) * 0.66,
  'k': Color((220,20,60)) * 0.66,
  'l': Color((255,140,0)) * 0.66,
  ';': Color((255,20,147)) * 0.66,
  "'": Color((0, 0, 0)),
  'z': Color((255, 0, 0)) * 0.33,
  'x': Color((0, 255, 0)) * 0.33,
  'c': Color((0, 0, 255)) * 0.33,
  'v': Color((255, 255, 0)) * 0.33,
  'b': Color((255, 0, 255)) * 0.33,
  'n': Color((0, 255, 255)) * 0.33,
  'm': Color((127,255,0)) * 0.33,
  ',': Color((220,20,60)) * 0.33,
  '.': Color((255,140,0)) * 0.33,
  '/': Color((255,20,147)) * 0.33,
  'up': Color((0, 0, 0)),
  'down': Color((0, 0, 0)),
  'left': Color((0, 0, 0)),
  'right': Color((0, 0, 0)),
  'tab': Color((0, 0, 0)),
  'enter': Color((0, 0, 0)),
  'del': Color((0, 0, 0)),
  'backspace': Color((0, 0, 0)),
  'space': Color((255, 255, 255)),
}

KEY_HSV_SHIFT_MAPPING = {
  'q': (10, 0, 0),
  'w': (20, 0, 0),
  'e': (30, 0, 0),
  'r': (40, 0, 0),
  't': (50, 0, 0),
  'y': (60, 0, 0),
  'u': (70, 0, 0),
  'i': (80, 0, 0),
  'o': (90, 0, 0),
  'p': (100,0, 0),
  '[': (0, 0, 0),
  ']': (0, 0, 0),
  'a': (0, -100, 0),
  's': (0, -80, 0),
  'd': (0, -60, 0),
  'f': (0, -40, 0),
  'g': (0, -20, 0),
  'h': (0, 20, 0),
  'j': (0, 40,0),
  'k': (0, 60,0),
  'l': (0, 80,0),
  ';': (0, 100,0),
  "'": (0, 0, 0),
  'z': (0, 0, -100),
  'x': (0, 0, -80),
  'c': (0, 0, -60),
  'v': (0, 0, -40),
  'b': (0, 0, -20),
  'n': (0, 0, 20),
  'm': (0, 0, 40),
  ',': (0, 0, 60),
  '.': (0, 0, 80),
  '/': (0, 0, 100),
  'up': (0, 0, 0),
  'down': (0, 0, 0),
  'left': (0, 0, 0),
  'right': (0, 0, 0),
  'tab': (0, 0, 0),
  'enter': (0, 0, 0),
  'del': (0, 0, 0),
  'backspace': (0, 0, 0),
  'space': (0, 0, -100),
}
