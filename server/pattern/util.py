from pattern import *
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

FLAT_GOODALE_TOP = 160
FLAT_GOODALE_SIDE = 97
FLAT_GOODALE_BOTTOM = 159
FLAT_GOODALE_LENGTH = FLAT_GOODALE_TOP + FLAT_GOODALE_SIDE + FLAT_GOODALE_BOTTOM

BASS = (0, 8)

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
