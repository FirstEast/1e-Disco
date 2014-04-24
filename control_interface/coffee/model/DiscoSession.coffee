do ->
  class com.firsteast.DiscoSession
    constructor: ->
      @beatModel = new com.firsteast.BeatModel()
      @realDiscoModel = new com.firsteast.DiscoModel()
      @mockDiscoModel = new com.firsteast.DiscoModel()

      @patternList = new Backbone.Collection()
      @patternList.model = com.firsteast.PatternModel

      @savedPatternList = new Backbone.Collection()
      @savedPatternList.model = com.firsteast.PatternModel

      @outputDeviceModel = new Backbone.Model()
      for device in com.firsteast.OUTPUT_DEVICES
        @outputDeviceModel.set(device, false)

      @inputDeviceModel = new Backbone.Model()
      for device in com.firsteast.INPUT_DEVICES
        @inputDeviceModel.set(device, false)

      @gifList = new Backbone.Collection()
      @imageList = new Backbone.Collection()

      @displayModel = new com.firsteast.DisplayModel()
      @hotkeyModel = new com.firsteast.HotkeyModel()

      @_configureHotkeys()

    _configureHotkeys: =>
      for key in com.firsteast.PATTERN_KEYS
        for device, prefix of com.firsteast.DEVICES_PREFIXES
          if prefix == ''
            Mousetrap.bind("#{key}", _.partial(@_setDevicePattern, key, device))
          else
            Mousetrap.bind("#{prefix}+#{key}", _.partial(@_setDevicePattern, key, device))

      for device, prefix of com.firsteast.DEVICES_PREFIXES
        if prefix != ''
          Mousetrap.bind(prefix, _.partial(@_setShownDevice, device), 'keydown')
          Mousetrap.bind(prefix, _.partial(@_setShownDevice, com.firsteast.OUTPUT_DEVICES[0]), 'keyup')

    _setShownDevice: (device) =>
      @hotkeyModel.set('shownDevice', device)

    _setDevicePattern: (key, device) =>
      name = @hotkeyModel.get('hotkeyPatterns')[device][key]
      pattern = @savedPatternList.where({saveName: name})[0].attributes
      pattern = $.extend(true, {}, pattern)
      # @realDiscoModel.set("#{device}Pattern", new com.firsteast.PatternModel(pattern))
      @realDiscoModel.set("ddfPattern", new com.firsteast.PatternModel(pattern))
