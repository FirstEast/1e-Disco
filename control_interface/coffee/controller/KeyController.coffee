do ->
  ALL_THE_KEYS = ['q','w','e','r','t','y','u','i','o','p','[',']','a','s','d','f','g','h','j','k','l',';',"'",'z','x','c','v','b','n','m',',','.','/','up','down','left','right','tab','enter','del','backspace','space']

  class com.firsteast.KeyController
    constructor: (options) ->
      $.extend @, Backbone.Events

      @_initializeSocket()
      @_bindHandlers()

    _initializeSocket: =>
      @socket = new WebSocket("ws://#{com.firsteast.WEBSOCKET_URL}:#{com.firsteast.KEY_SOCKET_PORT}/")

    _bindHandlers: =>
      for key in ALL_THE_KEYS
        Mousetrap.bind("#{key}", _.partial(@_downKey, key), 'keydown')
        Mousetrap.bind("#{key}", _.partial(@_upKey, key), 'keyup')

    _downKey: (key) =>
      data = {
        type: 'downKey'
        key: key
      }
      @_sendMessage(data)

    _upKey: (key) =>
      data = {
        type: 'upKey'
        key: key
      }
      @_sendMessage(data)

    _sendMessage: (data) =>
      msg = JSON.stringify(data)
      @socket.send(msg)