from pattern.color import *
from pattern.pattern import *
from pattern.util import *
from pattern.importer import loadSavedPatternFromFilename

from PIL import Image, ImageChops

import inspect, random

random.seed()

class Shuffle(TimedPattern):
  DEFAULT_PARAMS = {
    'Patterns': 4,
    'Pattern 0': 'default_linrainbow.json',
    'Pattern 1': 'default_linrainbow.json',
    'Pattern 2': 'default_linrainbow.json',
    'Pattern 3': 'default_linrainbow.json',
    'Pattern 4': 'default_linrainbow.json',
    'Pattern 5': 'default_linrainbow.json',
    'Pattern 6': 'default_linrainbow.json',
    'Pattern 7': 'default_linrainbow.json',
    'Pattern 8': 'default_linrainbow.json',
    'Pattern 9': 'default_linrainbow.json',
    'Duration 0': 200,
    'Duration 1': 150,
    'Duration 2': 150,
    'Duration 3': 150,
    'Duration 4': 150,
    'Duration 5': 150,
    'Duration 6': 150,
    'Duration 7': 150,
    'Duration 8': 150,
    'Duration 9': 150
  }

  DEFAULT_PARAMS.update(TimedPattern.DEFAULT_PARAMS)

  def __init__(self, beat, params):
    TimedPattern.__init__(self, beat, params)
    self.ticker = 0
    self.duration = 0
    self.pattern = None

  def renderFrame(self, device, frameCount):
    count = frameCount - self.ticker
    if count >= self.duration:
      self.ticker += self.duration
      i = random.randint(0, self.params['Patterns'] - 1)
      self.pattern = loadSavedPatternFromFilename(self.beat, self.params['Pattern ' + str(i)])
      self.duration = self.params['Duration ' + str(i)]
    return self.pattern.render(device)

class Queue(TimedPattern):
  DEFAULT_PARAMS = {
    'Patterns': 4,
    'Pattern 0': 'default_linrainbow.json',
    'Pattern 1': 'default_linrainbow.json',
    'Pattern 2': 'default_linrainbow.json',
    'Pattern 3': 'default_linrainbow.json',
    'Pattern 4': 'default_linrainbow.json',
    'Pattern 5': 'default_linrainbow.json',
    'Pattern 6': 'default_linrainbow.json',
    'Pattern 7': 'default_linrainbow.json',
    'Pattern 8': 'default_linrainbow.json',
    'Pattern 9': 'default_linrainbow.json',
    'Duration 0': 200,
    'Duration 1': 150,
    'Duration 2': 150,
    'Duration 3': 150,
    'Duration 4': 150,
    'Duration 5': 150,
    'Duration 6': 150,
    'Duration 7': 150,
    'Duration 8': 150,
    'Duration 9': 150
  }

  DEFAULT_PARAMS.update(TimedPattern.DEFAULT_PARAMS)

  def __init__(self, beat, params):
    TimedPattern.__init__(self, beat, params)
    self.ticker = 0
    self.duration = 0
    self.pattern = None
    self.patternID = -1

  def renderFrame(self, device, frameCount):
    count = frameCount - self.ticker
    if count >= self.duration:
      self.ticker += self.duration
      self.patternID = (self.patternID + 1) % self.params['Patterns']
      self.pattern = loadSavedPatternFromFilename(self.beat, self.params['Pattern ' + str(self.patternID)])
      self.duration = self.params['Duration ' + str(self.patternID)]
    return self.pattern.render(device)
