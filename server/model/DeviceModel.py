from Model import *

class DeviceModel(Model):
  def __init__(self):
    data = {\
      "goodale_lounge": False\
    }

    Model.__init__(self, data)