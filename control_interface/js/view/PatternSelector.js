(function() {
  var __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; },
    __hasProp = {}.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; };

  (function() {
    var _ref;
    return com.firsteast.PatternSelector = (function(_super) {
      __extends(PatternSelector, _super);

      function PatternSelector() {
        this._savePattern = __bind(this._savePattern, this);
        this._changeSelected = __bind(this._changeSelected, this);
        this._updateSelected = __bind(this._updateSelected, this);
        this.render = __bind(this.render, this);
        this.initialize = __bind(this.initialize, this);
        _ref = PatternSelector.__super__.constructor.apply(this, arguments);
        return _ref;
      }

      PatternSelector.prototype.className = 'patternSelector';

      PatternSelector.prototype.events = {
        'change select': '_changeSelected',
        'click .save-button': '_savePattern'
      };

      PatternSelector.prototype.initialize = function(options) {
        this.patternList = options.patternList;
        this.savedPatternList = options.savedPatternList;
        this.discoModel = options.discoModel;
        this.device = options.device;
        this.listenTo(this.patternList, 'reset', this.render);
        return this.listenTo(this.discoModel, "change:" + this.device + "Pattern", this._updateSelected);
      };

      PatternSelector.prototype.render = function() {
        var models, source, template,
          _this = this;
        this.$el.empty();
        source = $('#ddf-debug-template').html();
        template = Handlebars.compile(source);
        models = this.patternList.filter((function(x) {
          return x.get('DEVICES').indexOf(_this.device) >= 0;
        }));
        this.$el.append(template({
          patterns: models
        }));
        return this._updateSelected();
      };

      PatternSelector.prototype._updateSelected = function() {
        var _ref1;
        return this.$('select').val((_ref1 = this.discoModel.get("" + this.device + "Pattern")) != null ? _ref1.get('name') : void 0);
      };

      PatternSelector.prototype._changeSelected = function() {
        var name, pattern;
        name = this.$('select').val();
        pattern = this.patternList.where({
          name: name
        })[0].attributes;
        pattern = $.extend(true, {}, pattern);
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
  })();

}).call(this);
