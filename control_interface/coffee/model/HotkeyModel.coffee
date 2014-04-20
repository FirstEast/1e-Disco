do ->

  com.firsteast.PATTERN_KEYS = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
  com.firsteast.DEVICES_PREFIXES = 
    ddf: ''
    goodale: 'shift'
    bemis: 'ctrl'

  class com.firsteast.HotkeyModel extends Backbone.Model
    defaults: =>
      hotkeyPatterns = {}

      for device in com.firsteast.OUTPUT_DEVICES
        hotkeyPatterns[device] = {}

        for key in com.firsteast.PATTERN_KEYS
          hotkeyPatterns[device][key] = 'default_interpolation'

      shownDevice = com.firsteast.OUTPUT_DEVICES[0]

      attrs = 
        hotkeyPatterns: hotkeyPatterns
        shownDevice: shownDevice
      return attrs