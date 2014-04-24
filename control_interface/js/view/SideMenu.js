(function() {
  var __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; },
    __hasProp = {}.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; };

  (function() {
    return com.firsteast.SideMenu = (function(_super) {
      __extends(SideMenu, _super);

      function SideMenu() {
        this._toggleShowing = __bind(this._toggleShowing, this);
        this._toggleShowMock = __bind(this._toggleShowMock, this);
        this._toggleShowReal = __bind(this._toggleShowReal, this);
        this._triggerRealToMockSwap = __bind(this._triggerRealToMockSwap, this);
        this._triggerMockToRealSwap = __bind(this._triggerMockToRealSwap, this);
        this._changeHotkeyPattern = __bind(this._changeHotkeyPattern, this);
        this._updateSelectedHotkeyPatterns = __bind(this._updateSelectedHotkeyPatterns, this);
        this._importHotkeys = __bind(this._importHotkeys, this);
        this._updateString = __bind(this._updateString, this);
        this.render = __bind(this.render, this);
        this.initialize = __bind(this.initialize, this);
        return SideMenu.__super__.constructor.apply(this, arguments);
      }

      SideMenu.prototype.events = {
        'click .swap-mock-real': '_triggerMockToRealSwap',
        'click .swap-real-mock': '_triggerRealToMockSwap',
        'change .show-real': '_toggleShowReal',
        'change .show-mock': '_toggleShowMock',
        'click .handle': '_toggleShowing',
        'change .hotkey-patterns': '_changeHotkeyPattern',
        'click .hotkey-import': '_importHotkeys'
      };

      SideMenu.prototype.initialize = function(options) {
        this.model = options.model;
        this.realDiscoModel = options.realDiscoModel;
        this.mockDiscoModel = options.mockDiscoModel;
        this.savedPatternList = options.savedPatternList;
        this.hotkeyModel = options.hotkeyModel;
        this.showing = true;
        this.listenTo(this.savedPatternList, 'add remove reset', this.render);
        this.listenTo(this.hotkeyModel, 'change:shownDevice', this.render);
        return this.listenTo(this.hotkeyModel, 'hotkeyChange', this._updateString);
      };

      SideMenu.prototype.render = function() {
        var col, nonPartyWorthySaveModels, partyWorthySaveModels, saveModels, template;
        this.$el.empty();
        template = com.firsteast.templates['side-menu'];
        saveModels = _.sortBy(this.savedPatternList.filter((function(_this) {
          return function(x) {
            return x.get('DEVICES').indexOf('ddf') >= 0;
          };
        })(this)), function(x) {
          return x.get('saveName');
        });
        col = new Backbone.Collection(saveModels);
        partyWorthySaveModels = col.where({
          partyWorthy: true
        });
        nonPartyWorthySaveModels = col.where({
          partyWorthy: false
        });
        this.hotkeySet = this.hotkeyModel.get('hotkeyPatterns')[this.hotkeyModel.get('shownDevice')];
        this.$el.append(template({
          displayAttrs: this.model.attributes,
          partyWorthySaveModels: partyWorthySaveModels,
          nonPartyWorthySaveModels: nonPartyWorthySaveModels,
          hotkeySet: this.hotkeySet,
          hotkeyString: JSON.stringify(this.hotkeyModel.get('hotkeyPatterns'))
        }));
        return this._updateSelectedHotkeyPatterns();
      };

      SideMenu.prototype._updateString = function() {
        return this.$('.hotkey-export').val(JSON.stringify(this.hotkeyModel.get('hotkeyPatterns')));
      };

      SideMenu.prototype._importHotkeys = function() {
        this.hotkeyModel.set('hotkeyPatterns', JSON.parse(this.$('.hotkey-export').val()));
        return this.render();
      };

      SideMenu.prototype._updateSelectedHotkeyPatterns = function() {
        var el, key, _i, _len, _ref, _results;
        _ref = this.$('.hotkey-patterns');
        _results = [];
        for (_i = 0, _len = _ref.length; _i < _len; _i++) {
          el = _ref[_i];
          key = $(el).data().key;
          _results.push($(el).val(this.hotkeySet[key]));
        }
        return _results;
      };

      SideMenu.prototype._changeHotkeyPattern = function(event) {
        var fullSet, key;
        key = this.$(event.target).data().key;
        this.hotkeySet[key] = this.$(event.target).val();
        fullSet = this.hotkeyModel.get('hotkeyPatterns');
        fullSet[this.hotkeyModel.get('shownDevice')] = this.hotkeySet;
        this.hotkeyModel.set('hotkeyPatterns', fullSet);
        return this.hotkeyModel.trigger('hotkeyChange');
      };

      SideMenu.prototype._triggerMockToRealSwap = function() {
        var attributes, device, _i, _len, _ref, _results;
        _ref = com.firsteast.OUTPUT_DEVICES;
        _results = [];
        for (_i = 0, _len = _ref.length; _i < _len; _i++) {
          device = _ref[_i];
          attributes = this.mockDiscoModel.get("" + device + "Pattern").attributes;
          _results.push(this.realDiscoModel.set("" + device + "Pattern", new com.firsteast.PatternModel($.extend(true, {}, attributes))));
        }
        return _results;
      };

      SideMenu.prototype._triggerRealToMockSwap = function() {
        var attributes, device, _i, _len, _ref, _results;
        _ref = com.firsteast.OUTPUT_DEVICES;
        _results = [];
        for (_i = 0, _len = _ref.length; _i < _len; _i++) {
          device = _ref[_i];
          attributes = this.realDiscoModel.get("" + device + "Pattern").attributes;
          _results.push(this.mockDiscoModel.set("" + device + "Pattern", new com.firsteast.PatternModel($.extend(true, {}, attributes))));
        }
        return _results;
      };

      SideMenu.prototype._toggleShowReal = function() {
        return this.model.set('showReal', this.$('.show-real').prop('checked'));
      };

      SideMenu.prototype._toggleShowMock = function() {
        return this.model.set('showMock', this.$('.show-mock').prop('checked'));
      };

      SideMenu.prototype._toggleShowing = function() {
        if (this.showing) {
          this.$('.controls').hide();
          this.$el.addClass('hiding');
        } else {
          setTimeout(((function(_this) {
            return function() {
              return _this.$('.controls').show();
            };
          })(this)), 500);
          this.$el.removeClass('hiding');
        }
        return this.showing = !this.showing;
      };

      return SideMenu;

    })(Backbone.View);
  })();

}).call(this);
