(function() {
  var __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; },
    __hasProp = {}.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; };

  (function() {
    com.firsteast.PATTERN_KEYS = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'];
    com.firsteast.DEVICES_PREFIXES = {
      ddf: '',
      goodale: 'shift',
      bemis: 'ctrl'
    };
    return com.firsteast.HotkeyModel = (function(_super) {
      __extends(HotkeyModel, _super);

      function HotkeyModel() {
        this.defaults = __bind(this.defaults, this);
        return HotkeyModel.__super__.constructor.apply(this, arguments);
      }

      HotkeyModel.prototype.defaults = function() {
        var attrs, device, hotkeyPatterns, key, shownDevice, _i, _j, _len, _len1, _ref, _ref1;
        hotkeyPatterns = {};
        _ref = com.firsteast.OUTPUT_DEVICES;
        for (_i = 0, _len = _ref.length; _i < _len; _i++) {
          device = _ref[_i];
          hotkeyPatterns[device] = {};
          _ref1 = com.firsteast.PATTERN_KEYS;
          for (_j = 0, _len1 = _ref1.length; _j < _len1; _j++) {
            key = _ref1[_j];
            hotkeyPatterns[device][key] = 'default_interpolation';
          }
        }
        shownDevice = com.firsteast.OUTPUT_DEVICES[0];
        attrs = {
          hotkeyPatterns: hotkeyPatterns,
          shownDevice: shownDevice
        };
        return attrs;
      };

      return HotkeyModel;

    })(Backbone.Model);
  })();

}).call(this);
