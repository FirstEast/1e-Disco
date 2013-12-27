# Constants for convenient use.
GOODALE_WIDTH = 395
GOODALE_HEIGHT = 1
GOODALE_FORMAT = 'BGR'

DDF_WIDTH = 48
DDF_HEIGHT = 24
DDF_FORMAT = 'RGB'

BEMIS_WIDTH = 200
BEMIS_HEIGHT = 1
BEMIS_FORMAT = 'RGB'

class Pattern():

  DEFAULT_PARAMS = {
    # Your default parameter, such as:
    # 'Main Color': Color([255,0,0])
    # 
    # Note: do not set default parameters to None
  }

  # Override if you're using beat data
  USE_BEAT = False

  # Override to assign which devices this pattern is for
  DEVICES = ["goodale", "bemis", "ddf"]

  def render(self, device):
    '''
    Returns the next frame in the pattern for the given device
    '''
    pass

  def getDefaultParams(self): 
    '''
    Returns the map of param names to types
    '''
    return self.DEFAULT_PARAMS

  def getParams(self):
    '''
    Returns the chosen params for this pattern
    '''
    return self.params

  def setParam(self, name, val):
    '''
    Sets parameter 'name' to value 'val'
    '''
    self.params[name] = val