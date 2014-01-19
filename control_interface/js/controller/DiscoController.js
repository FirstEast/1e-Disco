(function() {
  var __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; };

  (function() {
    return com.firsteast.DiscoController = (function() {
      function DiscoController(options) {
        this._sendMessage = __bind(this._sendMessage, this);
        this._handlePatterns = __bind(this._handlePatterns, this);
        this._handleDevices = __bind(this._handleDevices, this);
        this._handleRender = __bind(this._handleRender, this);
        this._buildPatternList = __bind(this._buildPatternList, this);
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
          this._buildPatternList(JSON.parse(data.patternListData));
          return this._sendMessage({
            type: 'render'
          });
        } else if (data.type === 'render') {
          this._handleRender(data.renderData);
          return this._sendMessage({
            type: 'render'
          });
        } else if (data.type === 'devices') {
          return this._handleDevices(data.deviceData);
        } else if (data.type === 'realPatternData') {
          return this._handlePatterns(data.patternData);
        }
      };

      DiscoController.prototype._buildPatternList = function(patternMap) {
        var key, patterns, val;
        patterns = [];
        for (key in patternMap) {
          val = patternMap[key];
          val.name = key;
          patterns.push(val);
        }
        return this.session.patternList.reset(patterns);
      };

      DiscoController.prototype._handleRender = function(renderData) {
        this.session.realDiscoModel.set('frames', renderData.real);
        return this.session.mockDiscoModel.set('frames', renderData.mock);
      };

      DiscoController.prototype._handleDevices = function(deviceData) {
        this.session.inputDeviceModel.set(deviceData.inputDeviceModel);
        return this.session.outputDeviceModel.set(deviceData.outputDeviceModel);
      };

      DiscoController.prototype._handlePatterns = function(realPatternData) {
        var device, mockPatterns, obj, patterns, _ref;
        patterns = {};
        mockPatterns = {};
        _ref = realPatternData.realPatternClasses;
        for (device in _ref) {
          obj = _ref[device];
          obj.params = realPatternData.realPatternParams[device];
          patterns[device] = new com.firsteast.PatternModel(obj);
          mockPatterns[device] = new com.firsteast.PatternModel($.extend(true, {}, obj));
        }
        this.session.realDiscoModel.set('patterns', patterns);
        if (this.session.mockDiscoModel.get('patterns')['ddf'] == null) {
          return this.session.mockDiscoModel.set('patterns', mockPatterns);
        }
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
