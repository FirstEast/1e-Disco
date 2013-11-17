from ParameterTypes import *

class Pattern():

  GOODALE_WIDTH = 395
  GOODALE_HEIGHT = 1
  GOODALE_FORMAT = 'BGR'

  DDF_WIDTH = 48
  DDF_HEIGHT = 24
  DDF_FORMAT = 'RGB'

  def getNextFrame(self):
    '''
    Returns the next frame in the pattern
    '''
    pass

  def getExpectedParams(self): 
    '''
    Returns the map of param names to types
    '''
    return self.expectedParams

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