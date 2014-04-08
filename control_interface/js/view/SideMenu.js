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
        this.render = __bind(this.render, this);
        this.initialize = __bind(this.initialize, this);
        return SideMenu.__super__.constructor.apply(this, arguments);
      }

      SideMenu.prototype.events = {
        'click .swap-mock-real': '_triggerMockToRealSwap',
        'click .swap-real-mock': '_triggerRealToMockSwap',
        'change .show-real': '_toggleShowReal',
        'change .show-mock': '_toggleShowMock',
        'click .handle': '_toggleShowing'
      };

      SideMenu.prototype.initialize = function(options) {
        this.model = options.model;
        this.realDiscoModel = options.realDiscoModel;
        this.mockDiscoModel = options.mockDiscoModel;
        return this.showing = true;
      };

      SideMenu.prototype.render = function() {
        var template;
        this.$el.empty();
        template = com.firsteast.templates['side-menu'];
        return this.$el.append(template(this.model.attributes));
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
