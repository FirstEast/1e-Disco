import pkgutil
import inspect
import json

import pattern

# Map of device names to default pattern modules
DEFAULT_PATTERNS = {
  "goodale": "pattern.combo.Interpolation",
  "bemis": "pattern.combo.Interpolation",
  "ddf": "pattern.2d.MovingLine"
}

# Loads the first pattern class from a module path
def loadPatternFromModuleName(name):
  module = deepImport(name)
  for name, obj in inspect.getmembers(module):
    if inspect.isclass(obj) and issubclass(obj, pattern.Pattern) and obj.__name__ != 'Pattern':
      return obj

# Returns a map of all the devices to their default pattern classes
def getDefaultPatterns():
  patterns = {}
  for key in DEFAULT_PATTERNS:
    patterns[key] = loadPatternFromModuleName(DEFAULT_PATTERNS[key])
  return patterns

# Loads the map of all the pattern classes, mapped to the class names
def getPatternMap():
  all_modules = []

  # First get the top level modules in this directory
  top_modules = ['pattern.' + name for _, name, _ in pkgutil.iter_modules(['pattern'])]

  # Iterate going 1 level deep to find more modules
  for module in top_modules:
    all_modules += [(module + '.' + name) for _, name, _ in pkgutil.iter_modules([module.replace('.','/')])]
  all_modules += top_modules

  pattern_classes = {}
  for module_name in all_modules:
    module = deepImport(module_name)

    for name, obj in inspect.getmembers(module):
      if inspect.isclass(obj) and issubclass(obj, pattern.Pattern) and obj.__name__ != 'Pattern':
        pattern_classes[obj.__name__] = obj

  return pattern_classes

# Loads the pattenr map 
def getPatternMapJson():
  return json.dumps(getPatternMap(), default=(lambda x: x.__dict__))

def deepImport(name):
  m = __import__(name)
  for n in name.split(".")[1:]:
    m = getattr(m, n)
  return m