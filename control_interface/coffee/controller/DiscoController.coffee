do ->
  class com.firsteast.DiscoController
    constructor: (options) ->
      $.extend @, Backbone.Events

      @session = options.session

      @_initializeSocket()

      @listenTo @session.savedPatternList, 'add', @_savePattern

      @isActive = true

      window.onfocus = @_focusReturn
      window.onblur = @_focusLost

    _focusReturn: =>
      @isActive = true
      @_sendMessage {type: 'render'}

    _focusLost: =>
      @isActive = false

    _initializeSocket: =>
      @socket = new WebSocket("ws://#{com.firsteast.WEBSOCKET_URL}:#{com.firsteast.WEBSOCKET_PORT}/")
      @socket.onmessage = @_parseMessage

    _parseMessage: (message) =>
      data = JSON.parse(message.data)
      if data.type == 'init'
        @_buildPatternList(JSON.parse(data.patternListData))
        @_buildSavedPatternList(JSON.parse(data.savedPatternListData))
        @_buildGifList(data.gifList)
        @_buildImageList(data.imageList)
        @_sendMessage {type: 'render'} 
      else if data.type == 'render'
        @_handleRender(data.renderData)
        if @isActive
          @_sendMessage {type: 'render'}
      else if data.type == 'devices'
        @_handleDevices(data.deviceData)
      else if data.type == 'realPatternData'
        @_handlePatterns(data.patternData)

    _buildPatternList: (patternMap) =>
      patterns = []
      for key, val of patternMap
        val.name = key
        patterns.push(val)
      @session.patternList.reset(patterns)

    _buildSavedPatternList: (patternList) =>
      @session.savedPatternList.reset(patternList)

    _buildGifList: (gifList) =>
      result = []
      for gif in gifList
        result.push
          name: gif
      @session.gifList.reset(result)

    _buildImageList: (imageList) =>
      result = []
      for image in imageList
        result.push
          name: image
      @session.imageList.reset(result)

    _handleRender: (renderData) =>
      @session.realDiscoModel.set('frames', renderData.real)
      @session.mockDiscoModel.set('frames', renderData.mock)

    _handleDevices: (deviceData) =>
      @session.inputDeviceModel.set(deviceData.inputDeviceModel)
      @session.outputDeviceModel.set(deviceData.outputDeviceModel)

    _handlePatterns: (realPatternData) =>
      patterns = {}
      mockPatterns = {}
      for device, obj of realPatternData.realPatternClasses
        actualPattern = @session.patternList.where({name: obj})[0]
        attributes = $.extend(true, {}, actualPattern.attributes)
        attributes.params = realPatternData.realPatternParams[device]
        @session.realDiscoModel.set(device + 'Pattern', new com.firsteast.PatternModel(attributes))

        if not @session.mockDiscoModel.get(device + 'Pattern')?
          @session.mockDiscoModel.set(device + 'Pattern', new com.firsteast.PatternModel($.extend(true, {}, attributes)))

      # We have never had patterns before. Time to bind our listeners.
      for device in com.firsteast.OUTPUT_DEVICES
        @listenTo @session.realDiscoModel, "change:#{device}Pattern", _.partial(@_setRealPattern, "#{device}")
        @listenTo @session.mockDiscoModel, "change:#{device}Pattern", _.partial(@_setMockPattern, "#{device}")

    _savePattern: (pattern) =>
      data = {
        type: 'savePattern'
        patternData: pattern.attributes
      }
      @_sendMessage(data)

    _setRealPattern: (device) =>
      data = {
        type: 'setRealPattern'
        deviceName: device
        patternData: @session.realDiscoModel.get("#{device}Pattern").attributes
      }
      @_sendMessage(data)

    _setMockPattern: (device) =>
      data = {
        type: 'setMockPattern'
        deviceName: device
        patternData: @session.mockDiscoModel.get("#{device}Pattern").attributes
      }
      @_sendMessage(data)

    _updateRealPatternParams: (device) =>
      console.log @session.realDiscoModel.get(device + 'Pattern').attributes.params

    _sendMessage: (data) =>
      msg = JSON.stringify(data)
      @socket.send(msg)