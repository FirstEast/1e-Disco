do ->
  class com.firsteast.DiscoController
    constructor: (options) ->
      $.extend @, Backbone.Events

      @session = options.session

      @_initializeSocket()

      # TODO: listen to changes in the mock patterns

    _initializeSocket: =>
      @socket = new WebSocket("ws://#{com.firsteast.WEBSOCKET_URL}:#{com.firsteast.WEBSOCKET_PORT}/")
      @socket.onmessage = @_parseMessage

    _parseMessage: (message) =>
      data = JSON.parse(message.data)
      if data.type == 'init'
        console.log 'init'
        @_sendMessage 'renderOK'
      else if data.type == 'render'
        console.log 'render'
        @_sendMessage 'renderOK'
      else if data.type == 'devices'
        console.log 'devices'

    _updateSettings: (patient) =>
      @_sendMessage(patient.attributes)

    _sendMessage: (data) =>
      msg = JSON.stringify(data)
      @socket.send(msg)