(function() {
  var __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; },
    __hasProp = {}.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; };

  (function() {
    return com.firsteast.DiscoModel = (function(_super) {
      __extends(DiscoModel, _super);

      function DiscoModel() {
        this.defaults = __bind(this.defaults, this);
        return DiscoModel.__super__.constructor.apply(this, arguments);
      }

      DiscoModel.prototype.defaults = function() {
        var attrs, device, _i, _len, _ref;
        attrs = {
          frames: {}
        };
        _ref = com.firsteast.OUTPUT_DEVICES;
        for (_i = 0, _len = _ref.length; _i < _len; _i++) {
          device = _ref[_i];
          attrs.frames[device] = [];
          attrs[device + 'Pattern'] = null;
        }
        return attrs;
      };

      return DiscoModel;

    })(Backbone.Model);
  })();

}).call(this);
