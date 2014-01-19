from pattern import *
from PIL import Image

import math

# Device constants
GOODALE_WIDTH = 395
GOODALE_HEIGHT = 1
GOODALE_FORMAT = 'BGR'

DDF_WIDTH = 48
DDF_HEIGHT = 24

BEMIS_WIDTH = 261
BEMIS_HEIGHT = 1

FLAT_GOODALE_LENGTH = 159 + 97 + 160

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

def scaleToBucket(value, minVal, maxVal):
  v = (maxVal - minVal) * value + minVal
  v = min(max(v, minVal), maxVal)
  return int(math.floor(v))
