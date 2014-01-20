(function() {
  var __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; },
    __hasProp = {}.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; };

  (function() {
    var _ref;
    return com.firsteast.DiscoModel = (function(_super) {
      __extends(DiscoModel, _super);

      function DiscoModel() {
        this.defaults = __bind(this.defaults, this);
        _ref = DiscoModel.__super__.constructor.apply(this, arguments);
        return _ref;
      }

      DiscoModel.prototype.defaults = function() {
        var attrs, device, _i, _len, _ref1;
        attrs = {
          frames: {}
        };
        _ref1 = com.firsteast.OUTPUT_DEVICES;
        for (_i = 0, _len = _ref1.length; _i < _len; _i++) {
          device = _ref1[_i];
          attrs.frames[device] = [];
          attrs[device + 'Pattern'] = null;
        }
        return attrs;
      };

      return DiscoModel;

    })(Backbone.Model);
  })();

}).call(this);
