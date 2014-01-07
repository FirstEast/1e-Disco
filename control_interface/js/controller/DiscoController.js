(function() {
  var __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; };

  (function() {
    return com.firsteast.DiscoController = (function() {
      function DiscoController(options) {
        this._sendMessage = __bind(this._sendMessage, this);
        this._updateSettings = __bind(this._updateSettings, this);
        this._parseMessage = __bind(this._parseMessage, this);
        this._initializeSocket = __bind(this._initializeSocket, this);
        $.extend(this, Backbone.Events);
        this.session = options.session;
        this._initializeSocket();
      }

      DiscoController.prototype._initializeSocket = function() {
        this.socket = new WebSocket("ws://" + com.firsteast.WEBSOCKET_URL + ":" + com.firsteast.WEBSOCKET_PORT + "/");
        return this.socket.onmessage = this._parseMessage;
      };

      DiscoController.prototype._parseMessage = function(message) {
        var data;
        data = JSON.parse(message.data);
        if (data.type === 'init') {
          console.log('init');
          return this._sendMessage('renderOK');
        } else if (data.type === 'render') {
          console.log('render');
          return this._sendMessage('renderOK');
        } else if (data.type === 'devices') {
          return console.log('devices');
        }
      };

      DiscoController.prototype._updateSettings = function(patient) {
        return this._sendMessage(patient.attributes);
      };

      DiscoController.prototype._sendMessage = function(data) {
        var msg;
        msg = JSON.stringify(data);
        return this.socket.send(msg);
      };

      return DiscoController;

    })();
  })();

}).call(this);
