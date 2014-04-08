(function() {
  var __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; },
    __hasProp = {}.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; };

  (function() {
    return com.firsteast.BeatModel = (function(_super) {
      __extends(BeatModel, _super);

      function BeatModel() {
        this.defaults = __bind(this.defaults, this);
        return BeatModel.__super__.constructor.apply(this, arguments);
      }

      BeatModel.prototype.defaults = function() {
        return {
          centroid: 0,
          volume: 0,
          frequencies: []
        };
      };

      return BeatModel;

    })(Backbone.Model);
  })();

}).call(this);
