class Pattern():

  DEFAULT_PARAMS = {
    # Your default parameter, such as:
    # 'Main Color': Color([255,0,0])
    # 
    # Note: do not set default parameters to None
  }

  # Set if you're using beat data
  USE_BEAT = False

  # Set to assign which devices this pattern is for
  DEVICES = ["goodale", "bemis", "ddf"]

  def __init__(self, beat, params):
    '''
    Assign params to self.params. Make sure to call this in your subclass constructor!
    Also assigns beat to self.beat, in case your pattern uses it.
    '''
    self.params = self.DEFAULT_PARAMS
    self.params.update(params)
    self.beat = beat

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

class Frame():
  pass