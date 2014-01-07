from pattern.goodale.MovingLight import *
from pattern.goodale.BeatTest import *
from pattern.bemis.BemisMovingLight import *
from pattern.ddf.MovingLine import *

import pattern
import json
import Image

BUFFER_SIZE = 10
NUM_BANDS = 25

class DiscoSession():
  def __init__(self):
    # Map of devices to online status
    self.outputDeviceModel = {
      "goodale": False,
      "ddf": False,
      "bemis": False
    }

    self.inputDeviceModel = {
      "beat": False
    }

    # Initialize the beat model
    self.beatModel = BeatModel(BUFFER_SIZE, NUM_BANDS)

    self.patternModel = {
      "goodale": MovingLightPattern(self.beatModel, {}),
      "ddf": MovingLinePattern(self.beatModel, {}),
      "bemis": BemisMovingLightPattern(self.beatModel, {})
    }

# This is kind of stupid
class BeatModel():
  def __init__(self, buffer_size, num_bands):
    self.buffer_size = buffer_size
    self.num_bands = num_bands

    self.leftCentroids = [0] * buffer_size
    self.leftVolumes = [0] * buffer_size
    self.leftFrequencies = [[0] * num_bands] * buffer_size

    self.rightCentroids = [0] * buffer_size
    self.rightVolumes = [0] * buffer_size
    self.rightFrequencies = [[0] * num_bands] * buffer_size

  def getNormalizedCentroids(self, index):
    leftMin = min(self.leftCentroids)
    leftMax = max(self.leftCentroids)
    leftCent = self.leftCentroids[index]

    rightMin = min(self.rightCentroids)
    rightMax = max(self.rightCentroids)
    rightCent = self.rightCentroids[index]

    if (rightMax - rightMin) == 0:
      normRightCent = 0
    else:
      normRightCent = (rightCent - rightMin) / (rightMax - rightMin)

    if (leftMax - leftMin) == 0:
      normLeftCent = 0
    else:
      normLeftCent = (leftCent - leftMin) / (leftMax - leftMin)
    return [normLeftCent, normRightCent]

  def updateData(self, leftCentroid, leftVolume, leftFrequencies,\
                  rightCentroid, rightVolume, rightFrequencies):
    self.leftCentroids.pop()
    self.leftVolumes.pop()
    self.leftFrequencies.pop()
    self.rightCentroids.pop()
    self.rightVolumes.pop()
    self.rightFrequencies.pop()

    self.leftCentroids.insert(0, leftCentroid)
    self.leftVolumes.insert(0, leftVolume)
    self.leftFrequencies.insert(0, leftFrequencies)
    self.rightCentroids.insert(0, rightCentroid)
    self.rightVolumes.insert(0, rightVolume)
    self.rightFrequencies.insert(0, rightFrequencies)