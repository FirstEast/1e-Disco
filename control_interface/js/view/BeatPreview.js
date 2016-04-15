(function() {
  var __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; },
    __hasProp = {}.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; };

  (function() {
    return com.firsteast.BeatPreview = (function(_super) {
      __extends(BeatPreview, _super);

      function BeatPreview() {
        this.render = __bind(this.render, this);
        this.initialize = __bind(this.initialize, this);
        return BeatPreview.__super__.constructor.apply(this, arguments);
      }

      BeatPreview.prototype.className = 'beat-preview';

      BeatPreview.prototype.initialize = function(options) {
        var i, width, _i;
        this.model = options.model;
        this.$el.append('<div class="bar-container"/>');
        width = Math.floor(100 / 48) + '%';
        for (i = _i = 0; _i <= 48; i = ++_i) {
          this.$('.bar-container').append($('<div class="bar"/>').css('width', width));
        }
        return this.listenTo(this.model, 'change', this.render);
      };

      BeatPreview.prototype.render = function() {
        var $bars, freqs, i, _i, _ref, _results;
        freqs = this.model.get('frequencies');
        $bars = this.$('.bar');
        _results = [];
        for (i = _i = 0, _ref = freqs.length; 0 <= _ref ? _i <= _ref : _i >= _ref; i = 0 <= _ref ? ++_i : --_i) {
          _results.push($($bars[i]).css('height', ((Math.min((freqs[i] - 0.66) * 3, 1)) * 100 + 1) + '%'));
        }
        return _results;
      };

      return BeatPreview;

    })(Backbone.View);
  })();

}).call(this);
