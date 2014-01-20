do ->
  class com.firsteast.DiscoController
    constructor: (options) ->
      $.extend @, Backbone.Events

      @session = options.session

      @_initializeSocket()

      @listenTo @session.realDiscoModel, 'change:patterns', @_setRealPattern

    _initializeSocket: =>
      @socket = new WebSocket("ws://#{com.firsteast.WEBSOCKET_URL}:#{com.firsteast.WEBSOCKET_PORT}/")
      @socket.onmessage = @_parseMessage

    _parseMessage: (message) =>
      data = JSON.parse(message.data)
      if data.type == 'init'
        @_buildPatternList(JSON.parse(data.patternListData))
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
        patterns[device] = new com.firsteast.PatternModel(actualPattern.attributes)
        mockPatterns[device] = new com.firsteast.PatternModel($.extend(true, {}, actualPattern))
      @session.realDiscoModel.set('patterns', patterns)

      if not @session.mockDiscoModel.get('patterns')['ddf']?
        @session.mockDiscoModel.set('patterns', mockPatterns)

    _setRealPattern: =>
      for key, val of @session.realDiscoModel.get('patterns')
        data = {
          type: 'setRealPattern'
          deviceName: key
          patternData: val.attributes
        }
        console.log data
        @_sendMessage(data)

    _sendMessage: (data) =>
      msg = JSON.stringify(data)
      @socket.send(msg)