(function() {
  var __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; },
    __hasProp = {}.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; };

  (function() {
    return com.firsteast.DisplayModel = (function(_super) {
      __extends(DisplayModel, _super);

      function DisplayModel() {
        this.defaults = __bind(this.defaults, this);
        return DisplayModel.__super__.constructor.apply(this, arguments);
      }

      DisplayModel.prototype.defaults = function() {
        var attrs, device, _i, _len, _ref;
        attrs = {
          showReal: true,
          showMock: false
        };
        _ref = com.firsteast.OUTPUT_DEVICES;
        for (_i = 0, _len = _ref.length; _i < _len; _i++) {
          device = _ref[_i];
          attrs["show" + device] = true;
        }
        return attrs;
      };

      return DisplayModel;

    })(Backbone.Model);
  })();

}).call(this);
