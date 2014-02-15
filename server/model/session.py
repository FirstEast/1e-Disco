from pattern.importer import *

import pattern

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

    # Get the default patterns
    defaultPatterns = getDefaultPatterns()
    self.patternModel = {
      "goodale": defaultPatterns["goodale"](),
      "ddf": defaultPatterns["ddf"](),
      "bemis": defaultPatterns["bemis"]()
    }

  def getPattern(self, deviceName):
    return self.patternModel[deviceName]

  def setPattern(self, deviceName, pattern):
    self.patternModel[deviceName] = pattern