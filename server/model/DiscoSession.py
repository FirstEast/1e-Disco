from DeviceModel import *
from pattern.goodale.MovingLight import *
from pattern.ddf.MovingLine import *

class DiscoSession():
  def __init__(self):
    self.deviceModel = DeviceModel()
    self.goodalePattern = MovingLightPattern({})
    self.ddfPattern = MovingLinePattern({})