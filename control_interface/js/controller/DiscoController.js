(function() {
  var __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; };

  (function() {
    return com.firsteast.DiscoController = (function() {
      function DiscoController(options) {
        this._sendMessage = __bind(this._sendMessage, this);
        this._setRealPattern = __bind(this._setRealPattern, this);
        this._handlePatterns = __bind(this._handlePatterns, this);
        this._handleDevices = __bind(this._handleDevices, this);
        this._handleRender = __bind(this._handleRender, this);
        this._buildPatternList = __bind(this._buildPatternList, this);
        this._parseMessage = __bind(this._parseMessage, this);
        this._initializeSocket = __bind(this._initializeSocket, this);
        $.extend(this, Backbone.Events);
        this.session = options.session;
        this._initializeSocket();
        this.listenTo(this.session.realDiscoModel, 'change:patterns', this._setRealPattern);
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
        var actualPattern, device, mockPatterns, obj, patterns, _ref;
        patterns = {};
        mockPatterns = {};
        _ref = realPatternData.realPatternClasses;
        for (device in _ref) {
          obj = _ref[device];
          obj.params = realPatternData.realPatternParams[device];
          actualPattern = this.session.patternList.where({
            name: obj
          })[0];
          patterns[device] = new com.firsteast.PatternModel(actualPattern.attributes);
          mockPatterns[device] = new com.firsteast.PatternModel($.extend(true, {}, actualPattern));
        }
        this.session.realDiscoModel.set('patterns', patterns);
        if (this.session.mockDiscoModel.get('patterns')['ddf'] == null) {
          return this.session.mockDiscoModel.set('patterns', mockPatterns);
        }
      };

      DiscoController.prototype._setRealPattern = function() {
        var data, key, val, _ref, _results;
        _ref = this.session.realDiscoModel.get('patterns');
        _results = [];
        for (key in _ref) {
          val = _ref[key];
          data = {
            type: 'setRealPattern',
            deviceName: key,
            patternData: val.attributes
          };
          console.log(data);
          _results.push(this._sendMessage(data));
        }
        return _results;
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
