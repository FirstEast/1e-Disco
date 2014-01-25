(function() {
  var __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; },
    __hasProp = {}.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; };

  (function() {
    var getHexStringFromRgb, getRgbFromHexString, _ref,
      _this = this;
    com.firsteast.PatternSelector = (function(_super) {
      __extends(PatternSelector, _super);

      function PatternSelector() {
        this._savePattern = __bind(this._savePattern, this);
        this._changeParams = __bind(this._changeParams, this);
        this._changeSavedSelected = __bind(this._changeSavedSelected, this);
        this._changeClassSelected = __bind(this._changeClassSelected, this);
        this._updateSelected = __bind(this._updateSelected, this);
        this._setParamValues = __bind(this._setParamValues, this);
        this._parseParams = __bind(this._parseParams, this);
        this.render = __bind(this.render, this);
        this.initialize = __bind(this.initialize, this);
        _ref = PatternSelector.__super__.constructor.apply(this, arguments);
        return _ref;
      }

      PatternSelector.prototype.className = 'patternSelector';

      PatternSelector.prototype.events = {
        'change .class-patterns': '_changeClassSelected',
        'change .saved-patterns': '_changeSavedSelected',
        'change .param-input': '_changeParams',
        'click .save-button': '_savePattern'
      };

      PatternSelector.prototype.initialize = function(options) {
        this.patternList = options.patternList;
        this.savedPatternList = options.savedPatternList;
        this.discoModel = options.discoModel;
        this.device = options.device;
        this.parameters = {};
        this.listenTo(this.patternList, 'reset', this.render);
        this.listenTo(this.savedPatternList, 'reset', this.render);
        return this.listenTo(this.discoModel, "change:" + this.device + "Pattern", this.render);
      };

      PatternSelector.prototype.render = function() {
        var currentPattern, models, parameters, saveModels, source, template, _ref1,
          _this = this;
        this.$el.empty();
        source = $('#ddf-debug-template').html();
        template = Handlebars.compile(source);
        models = this.patternList.filter((function(x) {
          return x.get('DEVICES').indexOf(_this.device) >= 0;
        }));
        saveModels = this.savedPatternList.filter(function(x) {
          return x.get('DEVICES').indexOf(_this.device) >= 0;
        });
        currentPattern = (_ref1 = this.discoModel.get("" + this.device + "Pattern")) != null ? _ref1.attributes : void 0;
        parameters = this._parseParams(_.defaults({}, currentPattern != null ? currentPattern.params : void 0, currentPattern != null ? currentPattern.DEFAULT_PARAMS : void 0));
        this.$el.append(template({
          device: this.device,
          patterns: models,
          savedPatterns: saveModels,
          currentPattern: currentPattern,
          parameters: parameters
        }));
        this._updateSelected();
        return this._setParamValues(parameters);
      };

      PatternSelector.prototype._parseParams = function(params) {
        var key, param, result, val;
        result = [];
        for (key in params) {
          val = params[key];
          param = {
            name: key
          };
          param.val = val;
          if (typeof val === "object") {
            if (val.RGBValues != null) {
              param.type = 'color';
              param.val = getHexStringFromRgb(param.val.RGBValues);
            }
          } else if (typeof val === "boolean") {
            param.type = 'checkbox';
          } else if (typeof val === "string") {
            if (val.indexOf('.json') >= 0) {
              param.pattern = true;
              param.val = param.val.split('.json')[0];
            } else if (val.indexOf('.gif') >= 0) {
              param.gif = true;
            } else if (val.indexOf('.jpg') >= 0 || val.indexOf('.png') >= 0) {
              param.image = true;
            } else {
              param.type = 'text';
            }
          } else if (typeof val === 'number' || !isNaN(val)) {
            param.type = 'number';
          } else {
            param.type = 'text';
          }
          result.push(param);
        }
        return result;
      };

      PatternSelector.prototype._setParamValues = function(params) {
        var param, _i, _len, _results;
        _results = [];
        for (_i = 0, _len = params.length; _i < _len; _i++) {
          param = params[_i];
          _results.push(this.$("[name='" + param.name + "']").val(param.val));
        }
        return _results;
      };

      PatternSelector.prototype._updateSelected = function() {
        var _ref1, _ref2, _ref3;
        if ((_ref1 = this.discoModel.get("" + this.device + "Pattern")) != null ? _ref1.get('saved') : void 0) {
          return this.$('select').val((_ref2 = this.discoModel.get("" + this.device + "Pattern")) != null ? _ref2.get('saveName') : void 0);
        } else {
          return this.$('select').val((_ref3 = this.discoModel.get("" + this.device + "Pattern")) != null ? _ref3.get('name') : void 0);
        }
      };

      PatternSelector.prototype._changeClassSelected = function() {
        var name, pattern;
        name = this.$('.class-patterns').val();
        pattern = this.patternList.where({
          name: name
        })[0].attributes;
        pattern = $.extend(true, {}, pattern);
        return this.discoModel.set("" + this.device + "Pattern", new com.firsteast.PatternModel(pattern));
      };

      PatternSelector.prototype._changeSavedSelected = function() {
        var name, pattern;
        name = this.$('.saved-patterns').val();
        pattern = this.savedPatternList.where({
          saveName: name
        })[0].attributes;
        pattern = $.extend(true, {}, pattern);
        return this.discoModel.set("" + this.device + "Pattern", new com.firsteast.PatternModel(pattern));
      };

      PatternSelector.prototype._changeParams = function() {
        var inp, input, params, pattern, _i, _len, _ref1;
        params = {};
        _ref1 = this.$('.param-input');
        for (_i = 0, _len = _ref1.length; _i < _len; _i++) {
          input = _ref1[_i];
          inp = $(input);
          if (inp.prop('type') === 'color') {
            params[inp.prop('name')] = {
              RGBValues: getRgbFromHexString(inp.val())
            };
          } else if (inp.prop('type') === 'checkbox') {
            params[inp.prop('name')] = inp.prop('checked');
          } else if (inp.data('type') === 'pattern') {
            params[inp.prop('name')] = inp.val() + '.json';
          } else if (inp.prop('type') === 'number') {
            params[inp.prop('name')] = parseFloat(inp.val());
          } else {
            params[inp.prop('name')] = inp.val();
          }
        }
        pattern = this.discoModel.get("" + this.device + "Pattern").attributes;
        pattern = $.extend(true, {}, pattern);
        pattern.params = params;
        return this.discoModel.set("" + this.device + "Pattern", new com.firsteast.PatternModel(pattern));
      };

      PatternSelector.prototype._savePattern = function() {
        var pattern, patternModel, saveName;
        saveName = this.$('.save-name-input').val();
        pattern = this.discoModel.get("" + this.device + "Pattern").attributes;
        pattern = $.extend(true, {}, pattern);
        pattern.saved = true;
        pattern.saveName = saveName;
        patternModel = new com.firsteast.PatternModel(pattern);
        return this.savedPatternList.add(patternModel);
      };

      return PatternSelector;

    })(Backbone.View);
    getRgbFromHexString = function(hex) {
      var blue, green, red;
      red = parseInt(hex.substring(1, 3), 16);
      green = parseInt(hex.substring(3, 5), 16);
      blue = parseInt(hex.substring(5, 7), 16);
      return [red, green, blue];
    };
    return getHexStringFromRgb = function(RGB) {
      var hex, total, val, _i, _len;
      total = "#";
      for (_i = 0, _len = RGB.length; _i < _len; _i++) {
        val = RGB[_i];
        hex = val.toString(16);
        if (hex.length === 1) {
          hex = '0' + hex;
        }
        total = total + hex;
      }
      return total;
    };
  })();

}).call(this);