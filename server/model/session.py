from pattern.importer import *

import pattern
import json
import numpy

BUFFER_SIZE = 4
NUM_BANDS = 48

class DiscoSession():
  def __init__(self):
    # Map of output devices to online status
    self.outputDeviceModel = {
      "goodale": False,
      "ddf": False,
      "bemis": False
    }

    # Map of input devices to online status
    self.inputDeviceModel = {
      "beat": False
    }

    # Initialize the beat model
    self.beatModel = BeatModel(BUFFER_SIZE, NUM_BANDS)

    # Get the default patterns
    defaultPatterns = getDefaultPatterns()
    self.patternModel = {
      "goodale": defaultPatterns["goodale"](self.beatModel, {}),
      "ddf": defaultPatterns["ddf"](self.beatModel, {}),
      "bemis": defaultPatterns["bemis"](self.beatModel, {})
    }

  def getPattern(self, deviceName):
    return self.patternModel[deviceName]

  def setPattern(self, deviceName, pattern):
    self.patternModel[deviceName] = pattern

class BeatModel():
  def __init__(self, buffer_size, num_bands):
    self.buffer_size = buffer_size
    self.num_bands = num_bands

    self.centroids = [0] * buffer_size
    self.volumes = [0] * buffer_size
    self.frequencies = [[0] * num_bands] * buffer_size

    self.avgVolume = 0
    self.avgCentroid = 0
    self.avgFreqs = [0] * num_bands

  def getNormalizedCentroids(self, index):
    cMin = min(self.centroids)
    cMax = max(self.centroids)
    cCent = self.centroids[index]

    if (cMax - cMin) == 0:
      normCent = 0
    else:
      normCent = (cCent - cMin) / (cMax - cMin)
    return normCent

  def updateData(self, centroid, volume, frequencies):
    self.centroids.pop()
    self.volumes.pop()
    self.frequencies.pop()

    self.centroids.insert(0, centroid)
    self.volumes.insert(0, volume)
    self.frequencies.insert(0, frequencies)

    self.avgVolume = float(numpy.mean(self.volumes))
    self.avgCentroid = float(numpy.mean(self.centroids))
    newAvgFreq = []
    for i in range(self.num_bands):
      total = 0
      for j in range(self.buffer_size):
        total += self.frequencies[j][i]
      newAvgFreq.append(total / self.buffer_size)
    self.avgFreqs = newAvgFreq

