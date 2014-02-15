(function() {
  var __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; },
    __hasProp = {}.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; };

  (function() {
    var _ref;
    return com.firsteast.SideMenu = (function(_super) {
      __extends(SideMenu, _super);

      function SideMenu() {
        this._triggerRealToMockSwap = __bind(this._triggerRealToMockSwap, this);
        this._triggerMockToRealSwap = __bind(this._triggerMockToRealSwap, this);
        this.render = __bind(this.render, this);
        this.initialize = __bind(this.initialize, this);
        _ref = SideMenu.__super__.constructor.apply(this, arguments);
        return _ref;
      }

      SideMenu.prototype.events = {
        'click .swap-mock-real': '_triggerMockToRealSwap',
        'click .swap-real-mock': '_triggerRealToMockSwap'
      };

      SideMenu.prototype.initialize = function(options) {
        this.model = options.model;
        this.realDiscoModel = options.realDiscoModel;
        return this.mockDiscoModel = options.mockDiscoModel;
      };

      SideMenu.prototype.render = function() {
        var source, template;
        this.$el.empty();
        source = $('#side-menu-template').html();
        template = Handlebars.compile(source);
        return this.$el.append(template(this.model.attributes));
      };

      SideMenu.prototype._triggerMockToRealSwap = function() {
        var attributes, device, _i, _len, _ref1, _results;
        _ref1 = com.firsteast.OUTPUT_DEVICES;
        _results = [];
        for (_i = 0, _len = _ref1.length; _i < _len; _i++) {
          device = _ref1[_i];
          attributes = this.mockDiscoModel.get("" + device + "Pattern").attributes;
          _results.push(this.realDiscoModel.set("" + device + "Pattern", new com.firsteast.PatternModel($.extend(true, {}, attributes))));
        }
        return _results;
      };

      SideMenu.prototype._triggerRealToMockSwap = function() {
        var attributes, device, _i, _len, _ref1, _results;
        _ref1 = com.firsteast.OUTPUT_DEVICES;
        _results = [];
        for (_i = 0, _len = _ref1.length; _i < _len; _i++) {
          device = _ref1[_i];
          attributes = this.realDiscoModel.get("" + device + "Pattern").attributes;
          _results.push(this.mockDiscoModel.set("" + device + "Pattern", new com.firsteast.PatternModel($.extend(true, {}, attributes))));
        }
        return _results;
      };

      return SideMenu;

    })(Backbone.View);
  })();

}).call(this);
