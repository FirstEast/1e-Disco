from pattern.goodale.MovingLight import *
from pattern.ddf.MovingLine import *

class DiscoSession():
  def __init__(self):
    # Map of devices to online status
    self.deviceModel = {
      "goodale": False,
      "ddf": False
    }

    # Starting patterns for each device
    self.goodalePattern = MovingLightPattern({})
    self.ddfPattern = MovingLinePattern({})