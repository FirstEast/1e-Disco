do ->
  class com.firsteast.DiscoController
    constructor: (options) ->
      $.extend @, Backbone.Events

      @session = options.session

      @_initializeSocket()

      for device in com.firsteast.OUTPUT_DEVICES
        @listenTo @session.realDiscoModel, "change:#{device}Pattern", _.partial(@_setRealPattern, "#{device}")

      @listenTo @session.savedPatternList, 'add', @_savePattern

    _initializeSocket: =>
      @socket = new WebSocket("ws://#{com.firsteast.WEBSOCKET_URL}:#{com.firsteast.WEBSOCKET_PORT}/")
      @socket.onmessage = @_parseMessage

    _parseMessage: (message) =>
      data = JSON.parse(message.data)
      if data.type == 'init'
        @_buildPatternList(JSON.parse(data.patternListData))
        @_buildSavedPatternList(JSON.parse(data.savedPatternListData))
        @_sendMessage {type: 'render'} 
      else if data.type == 'render'
        @_handleRender(data.renderData)
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
        obj.params = realPatternData.realPatternParams[device]
        actualPattern = @session.patternList.where({name: obj})[0]
        @session.realDiscoModel.set(device + 'Pattern', new com.firsteast.PatternModel(actualPattern.attributes))

        if not @session.mockDiscoModel.get(device + 'Pattern')?
          @session.mockDiscoModel.set(device + 'Pattern', new com.firsteast.PatternModel($.extend(true, {}, actualPattern.attributes)))

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
        patternData: @session.realDiscoModel.get(device + 'Pattern').attributes
      }
      @_sendMessage(data)

    _sendMessage: (data) =>
      msg = JSON.stringify(data)
      @socket.send(msg)