from color import *
import time

DEFAULT_RATE = 30 #FPS

class Pattern():
  '''
  Top level pattern class. Defines basic parameter setting and render function.
  '''

  DEFAULT_PARAMS = {
    # Your default parameters, such as:
    # 'Main Color': Color([255,0,0])
    #
    # If this dict is empty, your Pattern will not appear in the web UI.
    #
    # If a param is a list of some sort, then don't mutate the list in your
    # own params dict. Assign a new one. Copying objects is not easy children.
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
    self.params = {}
    self.params.update(self.DEFAULT_PARAMS)
    self.params.update(params)
    self.beat = beat

    self.paramUpdate('ALL')

  def render(self, device):
    '''
    Returns the next frame in the pattern for the given device
    '''
    pass

  def paramUpdate(self, paramName):
    '''
    Do any stuff that needs to be calculated from the params.
    Called when the params change.
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
    self.paramUpdate(name)

  def getClass(self):
    return self.__class__

class StaticPattern(Pattern):
  '''
  Static Pattern class. Handles caching of frames for static patterns.
  Children must implement renderNew.
  '''

  def __init__(self, beat, params):
    Pattern.__init__(self, beat, params)
    self.newParams = True
    self.frame = None

  def paramUpdate(self, paramName):
    self.newParams = True

  def render(self, device):
    if self.newParams:
      self.frame = self.renderFrame(device)
      self.newParams = False
    return self.frame.copy()

  def renderFrame(self, device):
    '''
    Returns frame based on the set parameters. Only called when params change.
    '''
    pass

class TimedPattern(Pattern):
  '''
  Timed Pattern class. Handles frame counting based on real world time.
  Used for time variant looping patterns.

  Children of this class must implement the renderFrame function, which will
  be called with a frame number argument and the device.
  '''

  DEFAULT_PARAMS = {
    'Rate': DEFAULT_RATE
  }

  def __init__(self, beat, params):
    Pattern.__init__(self, beat, params)
    self.lastTime = time.time() * 1000
    self.frame = 0

  def render(self, device):
    return self.renderFrame(device, self.getFrameCount())

  def getFrameCount(self):
    thisTime = time.time() * 1000
    inc = int((thisTime - self.lastTime) / float(1000.0 / int(self.params['Rate'])))
    if inc > 0:
      self.frame += inc
      self.lastTime = thisTime
    return self.frame

  def renderFrame(self, device, frameCount):
    pass

