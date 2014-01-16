from color import *

DEFAULT_RATE = 30 #FPS

class Pattern():
  '''
  Top level pattern class. Defines basic parameter setting and render function.
  '''

  DEFAULT_PARAMS = {
    # Your default parameter, such as:
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
    self.paramUpdate()

  def render(self, device):
    '''
    Returns the next frame in the pattern for the given device
    '''
    pass

  def paramUpdate(self):
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
    self.paramUpdate()

class StaticPattern(Pattern):
  '''
  Static Pattern class. Handles caching of frames for static patterns.
  Children must implement renderNew.
  '''

  def __init__(self, beat, params):
    Pattern.__init__(self, beat, params)
    self.newParams = True
    self.frame = None

  def render(self, device):
    if self.newParams:
      self.frame = self.renderFrame(device)
      self.newParams = False
    return self.frame

  def setParam(self, name, val):
    self.params[name] = val
    self.newParams = True

  def renderFrame(self, device):
    '''
    Returns frame based on the set parameters. Only called when params change.
    '''
    pass

class TimedPattern(Pattern):
  '''
  Timed Pattern class. Handles frame counting based on real world time and
  caching of each frame, so as to prevent avoidable computation. Used for
  time variant looping patterns.

  Children of this class must implement the renderFrame function, which will
  be called with a frame number argument if no data for that frame number is
  found in the cache. The cache is cleared whenever the parameters for this
  pattern change.

  Children of this class are also expected to set an instance variable
  'duration', which is the total number of frames in a single iteration of
  the pattern. This is likely dependent upon which device is being rendered,
  the parameters, etc. Update this variable accordingly using the setDuration
  function, as this will also clear the cache for you (if the new duration is
  different from the old duration).

  When determining the frame, this class will attempt to reference a 'Rate'
  parameter within the self.params dictionary. If no such parameter is found,
  the pattern will display at the framerate specified by DEFAULT_RATE (above).
  '''

  def __init__(self, beat, params):
    Pattern.__init__(self, beat, params)
    #TODO

  def render(self, device):
    pass

  def setParam(self, name, val):
    self.params[name] = val
    #TODO

  def renderFrame(self, device, frame):
    pass

class Frame():
  def __init__(self, colorArray):
    self.colorArray = colorArray
    self.height = len(colorArray)
    self.width = len(colorArray[0])

  def maskFrame(self, mask):
    if len(mask) != self.height or len(mask[0]) != self.width:
      raise TypeError

    newFrame = [[BLACK] * self.width] * self.height
    for i in range(self.height):
      for j in range(self.width):
        if mask[i][j] == BLACK:
          newFrame[i][j] = BLACK
        else:
          newFrame[i][j] = self.colorArray[i][j]
    return Frame(newFrame)

  def __add__(self, frame):
    if isinstance(frame, Frame):
      if len(frame) != self.height or len(frame[0]) != self.width:
        raise TypeError

      newFrame = [[BLACK] * self.width] * self.height
      for i in range(self.height):
        for j in range(self.width):
          newFrame[i][j] = self.colorArray[i][j] + frame[i][j]
      return Frame(newFrame)
    else:
      raise TypeError

  def __sub__(self, frame):
    if isinstance(frame, Frame):
      if len(frame) != self.height or len(frame[0]) != self.width:
        raise TypeError

      newFrame = [[BLACK] * self.width] * self.height
      for i in range(self.height):
        for j in range(self.width):
          newFrame[i][j] = self.colorArray[i][j] - frame[i][j]
      return Frame(newFrame)
    else:
      raise TypeError

  def __mul__(self, scalar):
    if type(scalar) is int or type(scalar) is float:
      newFrame = [[BLACK] * self.width] * self.height
      for i in range(self.height):
        for j in range(self.width):
          newFrame[i][j] = self.colorArray[i][j] * scalar
      return Frame(newFrame)
    else:
      raise TypeError

  def __div__(self, scalar):
    if type(scalar) is int or type(scalar) is float:
      newFrame = [[BLACK] * self.width] * self.height
      for i in range(self.height):
        for j in range(self.width):
          newFrame[i][j] = self.colorArray[i][j] / scalar
      return Frame(newFrame)
    else:
      raise TypeError

  def __len__(self):
    return len(self.colorArray)

  def __getitem__(self, index):
    return self.colorArray[index]