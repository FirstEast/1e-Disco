(function() {
  var __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; };

  (function() {
    var ALL_THE_KEYS;
    ALL_THE_KEYS = ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[', ']', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', "'", 'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/', 'up', 'down', 'left', 'right', 'tab', 'enter', 'del', 'backspace', 'space'];
    return com.firsteast.KeyController = (function() {
      function KeyController(options) {
        this._sendMessage = __bind(this._sendMessage, this);
        this._upKey = __bind(this._upKey, this);
        this._downKey = __bind(this._downKey, this);
        this._bindHandlers = __bind(this._bindHandlers, this);
        this._initializeSocket = __bind(this._initializeSocket, this);
        $.extend(this, Backbone.Events);
        this._initializeSocket();
        this._bindHandlers();
      }

      KeyController.prototype._initializeSocket = function() {
        return this.socket = new WebSocket("ws://" + com.firsteast.WEBSOCKET_URL + ":" + com.firsteast.KEY_SOCKET_PORT + "/");
      };

      KeyController.prototype._bindHandlers = function() {
        var key, _i, _len, _results;
        _results = [];
        for (_i = 0, _len = ALL_THE_KEYS.length; _i < _len; _i++) {
          key = ALL_THE_KEYS[_i];
          Mousetrap.bind("" + key, _.partial(this._downKey, key), 'keydown');
          _results.push(Mousetrap.bind("" + key, _.partial(this._upKey, key), 'keyup'));
        }
        return _results;
      };

      KeyController.prototype._downKey = function(key) {
        var data;
        data = {
          type: 'downKey',
          key: key
        };
        return this._sendMessage(data);
      };

      KeyController.prototype._upKey = function(key) {
        var data;
        data = {
          type: 'upKey',
          key: key
        };
        return this._sendMessage(data);
      };

      KeyController.prototype._sendMessage = function(data) {
        var msg;
        msg = JSON.stringify(data);
        return this.socket.send(msg);
      };

      return KeyController;

    })();
  })();

}).call(this);
