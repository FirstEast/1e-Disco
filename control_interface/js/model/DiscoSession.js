(function() {
  var __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; };

  (function() {
    return com.firsteast.DiscoSession = (function() {
      function DiscoSession() {
        this._setDevicePattern = __bind(this._setDevicePattern, this);
        this._setShownDevice = __bind(this._setShownDevice, this);
        this._configureHotkeys = __bind(this._configureHotkeys, this);
        var device, _i, _j, _len, _len1, _ref, _ref1;
        this.beatModel = new com.firsteast.BeatModel();
        this.realDiscoModel = new com.firsteast.DiscoModel();
        this.mockDiscoModel = new com.firsteast.DiscoModel();
        this.patternList = new Backbone.Collection();
        this.patternList.model = com.firsteast.PatternModel;
        this.savedPatternList = new Backbone.Collection();
        this.savedPatternList.model = com.firsteast.PatternModel;
        this.outputDeviceModel = new Backbone.Model();
        _ref = com.firsteast.OUTPUT_DEVICES;
        for (_i = 0, _len = _ref.length; _i < _len; _i++) {
          device = _ref[_i];
          this.outputDeviceModel.set(device, false);
        }
        this.inputDeviceModel = new Backbone.Model();
        _ref1 = com.firsteast.INPUT_DEVICES;
        for (_j = 0, _len1 = _ref1.length; _j < _len1; _j++) {
          device = _ref1[_j];
          this.inputDeviceModel.set(device, false);
        }
        this.gifList = new Backbone.Collection();
        this.imageList = new Backbone.Collection();
        this.displayModel = new com.firsteast.DisplayModel();
        this.hotkeyModel = new com.firsteast.HotkeyModel();
        this._configureHotkeys();
      }

      DiscoSession.prototype._configureHotkeys = function() {
        var device, key, prefix, _i, _len, _ref, _ref1, _ref2, _results;
        _ref = com.firsteast.PATTERN_KEYS;
        for (_i = 0, _len = _ref.length; _i < _len; _i++) {
          key = _ref[_i];
          _ref1 = com.firsteast.DEVICES_PREFIXES;
          for (device in _ref1) {
            prefix = _ref1[device];
            if (prefix === '') {
              Mousetrap.bind("" + key, _.partial(this._setDevicePattern, key, device));
            } else {
              Mousetrap.bind("" + prefix + "+" + key, _.partial(this._setDevicePattern, key, device));
            }
          }
        }
        _ref2 = com.firsteast.DEVICES_PREFIXES;
        _results = [];
        for (device in _ref2) {
          prefix = _ref2[device];
          if (prefix !== '') {
            Mousetrap.bind(prefix, _.partial(this._setShownDevice, device), 'keydown');
            _results.push(Mousetrap.bind(prefix, _.partial(this._setShownDevice, com.firsteast.OUTPUT_DEVICES[0]), 'keyup'));
          } else {
            _results.push(void 0);
          }
        }
        return _results;
      };

      DiscoSession.prototype._setShownDevice = function(device) {
        return this.hotkeyModel.set('shownDevice', device);
      };

      DiscoSession.prototype._setDevicePattern = function(key, device) {
        var name, pattern;
        name = this.hotkeyModel.get('hotkeyPatterns')[device][key];
        pattern = this.savedPatternList.where({
          saveName: name
        })[0].attributes;
        pattern = $.extend(true, {}, pattern);
        return this.realDiscoModel.set("" + device + "Pattern", new com.firsteast.PatternModel(pattern));
      };

      return DiscoSession;

    })();
  })();

}).call(this);
