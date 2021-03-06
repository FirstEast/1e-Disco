(function() {
  var __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; };

  (function() {
    return com.firsteast.DiscoController = (function() {
      function DiscoController(options) {
        this._sendMessage = __bind(this._sendMessage, this);
        this._updateMockPatternParams = __bind(this._updateMockPatternParams, this);
        this._updateRealPatternParams = __bind(this._updateRealPatternParams, this);
        this._setMockPattern = __bind(this._setMockPattern, this);
        this._setRealPattern = __bind(this._setRealPattern, this);
        this._savePattern = __bind(this._savePattern, this);
        this._handlePatterns = __bind(this._handlePatterns, this);
        this._handleDevices = __bind(this._handleDevices, this);
        this._handleRender = __bind(this._handleRender, this);
        this._handleAudio = __bind(this._handleAudio, this);
        this._buildImageList = __bind(this._buildImageList, this);
        this._buildGifList = __bind(this._buildGifList, this);
        this._buildSavedPatternList = __bind(this._buildSavedPatternList, this);
        this._buildPatternList = __bind(this._buildPatternList, this);
        this._parseMessage = __bind(this._parseMessage, this);
        this._initializeSocket = __bind(this._initializeSocket, this);
        this._focusLost = __bind(this._focusLost, this);
        this._focusReturn = __bind(this._focusReturn, this);
        $.extend(this, Backbone.Events);
        this.session = options.session;
        this._initializeSocket();
        this.listenTo(this.session.savedPatternList, 'add', this._savePattern);
        this.isActive = true;
        window.onfocus = this._focusReturn;
        window.onblur = this._focusLost;
      }

      DiscoController.prototype._focusReturn = function() {
        this.isActive = true;
        this._sendMessage({
          type: 'render'
        });
        return this._sendMessage({
          type: 'audio'
        });
      };

      DiscoController.prototype._focusLost = function() {
        return this.isActive = false;
      };

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
          this._buildGifList(data.gifList);
          this._buildImageList(data.imageList);
          this._sendMessage({
            type: 'render'
          });
          return this._sendMessage({
            type: 'audio'
          });
        } else if (data.type === 'render') {
          this._handleRender(data.renderData);
          if (this.isActive) {
            return setTimeout(_.partial(this._sendMessage, {
              type: 'render'
            }), 200);
          }
        } else if (data.type === 'audio') {
          this._handleAudio(data.audioData);
          if (this.isActive) {
            return setTimeout(_.partial(this._sendMessage, {
              type: 'audio'
            }), 200);
          }
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

      DiscoController.prototype._buildGifList = function(gifList) {
        var gif, result, _i, _len;
        result = [];
        for (_i = 0, _len = gifList.length; _i < _len; _i++) {
          gif = gifList[_i];
          result.push({
            name: gif
          });
        }
        return this.session.gifList.reset(result);
      };

      DiscoController.prototype._buildImageList = function(imageList) {
        var image, result, _i, _len;
        result = [];
        for (_i = 0, _len = imageList.length; _i < _len; _i++) {
          image = imageList[_i];
          result.push({
            name: image
          });
        }
        return this.session.imageList.reset(result);
      };

      DiscoController.prototype._handleAudio = function(audioData) {
        return this.session.beatModel.set(audioData);
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
        var actualPattern, attributes, device, mockPatterns, obj, patterns, _i, _len, _ref, _ref1, _results;
        patterns = {};
        mockPatterns = {};
        _ref = realPatternData.realPatternClasses;
        for (device in _ref) {
          obj = _ref[device];
          actualPattern = this.session.patternList.where({
            name: obj
          })[0];
          attributes = $.extend(true, {}, actualPattern.attributes);
          attributes.params = realPatternData.realPatternParams[device];
          this.session.realDiscoModel.set(device + 'Pattern', new com.firsteast.PatternModel(attributes));
          if (this.session.mockDiscoModel.get(device + 'Pattern') == null) {
            this.session.mockDiscoModel.set(device + 'Pattern', new com.firsteast.PatternModel($.extend(true, {}, attributes)));
          }
        }
        _ref1 = com.firsteast.OUTPUT_DEVICES;
        _results = [];
        for (_i = 0, _len = _ref1.length; _i < _len; _i++) {
          device = _ref1[_i];
          this.listenTo(this.session.realDiscoModel, "change:" + device + "Pattern", _.partial(this._setRealPattern, "" + device));
          this.listenTo(this.session.mockDiscoModel, "change:" + device + "Pattern", _.partial(this._setMockPattern, "" + device));
          this.listenTo(this.session.realDiscoModel, "" + device + "ChangeParam", _.partial(this._updateRealPatternParams, "" + device));
          _results.push(this.listenTo(this.session.mockDiscoModel, "" + device + "ChangeParam", _.partial(this._updateMockPatternParams, "" + device)));
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
          patternData: this.session.realDiscoModel.get("" + device + "Pattern").attributes
        };
        return this._sendMessage(data);
      };

      DiscoController.prototype._setMockPattern = function(device) {
        var data;
        data = {
          type: 'setMockPattern',
          deviceName: device,
          patternData: this.session.mockDiscoModel.get("" + device + "Pattern").attributes
        };
        return this._sendMessage(data);
      };

      DiscoController.prototype._updateRealPatternParams = function(device, param) {
        var data;
        data = {
          type: 'realParam',
          deviceName: device,
          paramName: param.name,
          paramVal: param.val
        };
        return this._sendMessage(data);
      };

      DiscoController.prototype._updateMockPatternParams = function(device, param) {
        var data;
        data = {
          type: 'mockParam',
          deviceName: device,
          paramName: param.name,
          paramVal: param.val
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
