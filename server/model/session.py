from pattern.goodale.MovingLight import *
from pattern.goodale.BeatTest import *
from pattern.bemis.BemisMovingLight import *
from pattern.ddf.MovingLine import *

BUCKET_SIZE = 10
BUFFER_SIZE = 10

class DiscoSession():
  def __init__(self):
    # Map of devices to online status
    self.deviceModel = {
      "goodale": False,
      "ddf": False,
      "bemis": False,
      "beat": False
    }

    # Initialize the beat model
    self.beatModel = BeatModel(BUCKET_SIZE, BUFFER_SIZE)

    # Starting patterns for each device
    self.goodalePattern = BeatTestPattern(self.beatModel, {})
    self.ddfPattern = MovingLinePattern(self.beatModel, {})
    self.bemisPattern = BemisMovingLightPattern(self.beatModel, {})

# This is kind of stupid
class BeatModel():
  def __init__(self, buffer_size, bucket_size):
    self.buffer_size = buffer_size
    self.bucket_size = bucket_size

    self.leftCentroids = [0] * buffer_size
    self.leftVolumes = [0] * buffer_size
    self.leftFrequencies = [[0] * bucket_size] * buffer_size

    self.rightCentroids = [0] * buffer_size
    self.rightVolumes = [0] * buffer_size
    self.rightFrequencies = [[0] * bucket_size] * buffer_size

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