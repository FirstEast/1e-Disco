(function() {
  var __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; },
    __hasProp = {}.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; };

  (function() {
    var _ref;
    return com.firsteast.PatternModel = (function(_super) {
      __extends(PatternModel, _super);

      function PatternModel() {
        this.defaults = __bind(this.defaults, this);
        _ref = PatternModel.__super__.constructor.apply(this, arguments);
        return _ref;
      }

      PatternModel.prototype.defaults = function() {
        return {
          __module__: null,
          name: null,
          USE_BEAT: false,
          DEVICES: com.firsteast.OUTPUT_DEVICES,
          DEFAULT_PARAMS: {},
          params: {},
          saved: false,
          saveName: ''
        };
      };

      return PatternModel;

    })(Backbone.Model);
  })();

}).call(this);
