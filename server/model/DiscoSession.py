from DeviceModel import *

class DiscoSession():
  def __init__(self):
    self.deviceModel = DeviceModel()
    self.goodaleArduinoModel = Model({"state": "off"})