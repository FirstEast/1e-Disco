import pkgutil
import inspect
import json
import glob

import pattern

# Map of device names to default pattern modules
DEFAULT_PATTERNS = {
  "goodale": "pattern.timed.basic_Interpolation",
  "bemis": "pattern.timed.basic_Interpolation",
  "ddf": "pattern.timed.basic_Interpolation"
}

SUPER_PATTERN_CLASSES = {
  'Pattern', 'StaticPattern', 'TimedPattern'
}

PATTERN_SAVE_DIR = 'pattern/saved/'

# Returns a pattern class from a name formatted as "module.path_className"
def loadPatternFromModuleClassName(name):
  moduleName = name.split('_')[0]
  module = deepImport(moduleName)
  for n, obj in inspect.getmembers(module):
    if inspect.isclass(obj) and issubclass(obj, pattern.Pattern) and obj.__name__ == name.split('_')[1]:
      return obj

# Returns a pattern instance from a saved pattern name
def loadSavedPattern(beat, patternData):
  moduleClassName = patternData['__module__'] + '_' + patternData['name']
  pattern = loadPatternFromModuleClassName(moduleClassName)(beat, patternData['params'])
  return pattern

def loadSavedPatternFromFilename(beat, fileName):
  f = open(PATTERN_SAVE_DIR + fileName)
  data = json.load(f)
  f.close()
  return loadSavedPattern(beat, data)

# Returns a map of all the devices to their default pattern classes
def getDefaultPatterns():
  patterns = {}
  for key in DEFAULT_PATTERNS:
    patterns[key] = loadPatternFromModuleClassName(DEFAULT_PATTERNS[key])
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
      if inspect.isclass(obj) and issubclass(obj, pattern.Pattern) and (obj.__name__ not in SUPER_PATTERN_CLASSES):
        pattern_classes[obj.__name__] = obj

  return pattern_classes

# Loads the pattern map as a JSON string for the web UI
def getPatternMapJson():
  return json.dumps(getPatternMap(), default=(lambda x: x.__dict__))

def getSavedPatternJson():
  result = []
  saveFiles = glob.glob(PATTERN_SAVE_DIR + '*.json')
  for saveFile in saveFiles:
    f = open(saveFile)
    result.append(json.load(f))
    f.close()
  return json.dumps(result)

def deepImport(name):
  m = __import__(name)
  for n in name.split(".")[1:]:
    m = getattr(m, n)
  return m