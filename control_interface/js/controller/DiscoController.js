(function() {
  var __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; };

  (function() {
    return com.firsteast.DiscoController = (function() {
      function DiscoController(options) {
        this._sendMessage = __bind(this._sendMessage, this);
        this._setRealPattern = __bind(this._setRealPattern, this);
        this._savePattern = __bind(this._savePattern, this);
        this._handlePatterns = __bind(this._handlePatterns, this);
        this._handleDevices = __bind(this._handleDevices, this);
        this._handleRender = __bind(this._handleRender, this);
        this._buildSavedPatternList = __bind(this._buildSavedPatternList, this);
        this._buildPatternList = __bind(this._buildPatternList, this);
        this._parseMessage = __bind(this._parseMessage, this);
        this._initializeSocket = __bind(this._initializeSocket, this);
        var device, _i, _len, _ref;
        $.extend(this, Backbone.Events);
        this.session = options.session;
        this._initializeSocket();
        _ref = com.firsteast.OUTPUT_DEVICES;
        for (_i = 0, _len = _ref.length; _i < _len; _i++) {
          device = _ref[_i];
          this.listenTo(this.session.realDiscoModel, "change:" + device + "Pattern", _.partial(this._setRealPattern, "" + device));
        }
        this.listenTo(this.session.savedPatternList, 'add', this._savePattern);
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
          this._buildSavedPatternList(JSON.parse(data.savedPatternListData));
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

      DiscoController.prototype._buildSavedPatternList = function(patternList) {
        return this.session.savedPatternList.reset(patternList);
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
        var actualPattern, device, mockPatterns, obj, patterns, _ref, _results;
        patterns = {};
        mockPatterns = {};
        _ref = realPatternData.realPatternClasses;
        _results = [];
        for (device in _ref) {
          obj = _ref[device];
          obj.params = realPatternData.realPatternParams[device];
          actualPattern = this.session.patternList.where({
            name: obj
          })[0];
          this.session.realDiscoModel.set(device + 'Pattern', new com.firsteast.PatternModel(actualPattern.attributes));
          if (this.session.mockDiscoModel.get(device + 'Pattern') == null) {
            _results.push(this.session.mockDiscoModel.set(device + 'Pattern', new com.firsteast.PatternModel($.extend(true, {}, actualPattern.attributes))));
          } else {
            _results.push(void 0);
          }
        }
        return _results;
      };

      DiscoController.prototype._savePattern = function(pattern) {
        var data;
        data = {
          type: 'savePattern',
          patternData: pattern.attributes
        };
        return this._sendMessage(data);
      };

      DiscoController.prototype._setRealPattern = function(device) {
        var data;
        data = {
          type: 'setRealPattern',
          deviceName: device,
          patternData: this.session.realDiscoModel.get(device + 'Pattern').attributes
        };
        return this._sendMessage(data);
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
