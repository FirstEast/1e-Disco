from Model import *

class DeviceModel(Model):
  def __init__(self):
    data = {
      "goodale": False,
      "ddf": False
    }

    Model.__init__(self, data)