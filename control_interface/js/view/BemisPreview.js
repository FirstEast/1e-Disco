(function() {
  var __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; },
    __hasProp = {}.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; };

  (function() {
    var _ref;
    return com.firsteast.BemisPreview = (function(_super) {
      __extends(BemisPreview, _super);

      function BemisPreview() {
        this.renderCanvas = __bind(this.renderCanvas, this);
        this.render = __bind(this.render, this);
        this.initialize = __bind(this.initialize, this);
        _ref = BemisPreview.__super__.constructor.apply(this, arguments);
        return _ref;
      }

      BemisPreview.prototype.tagName = 'canvas';

      BemisPreview.prototype.className = 'bemisPreview';

      BemisPreview.prototype.initialize = function(options) {
        this.listenTo(this.model, 'change:frames', this.renderCanvas);
        this.width = options.width;
        return this.height = options.height;
      };

      BemisPreview.prototype.render = function() {
        var canvas;
        canvas = this.$el[0];
        this.context = canvas.getContext('2d');
        canvas.width = this.width;
        canvas.height = this.height;
        return this.squareWidth = ((this.width / com.firsteast.BEMIS_WIDTH) | 0) - 1;
      };

      BemisPreview.prototype.renderCanvas = function() {
        var RGBArray, blue, green, i, red, _i, _ref1, _results;
        RGBArray = this.model.get('frames')['bemis'];
        _results = [];
        for (i = _i = 0, _ref1 = com.firsteast.BEMIS_WIDTH; 0 <= _ref1 ? _i <= _ref1 : _i >= _ref1; i = 0 <= _ref1 ? ++_i : --_i) {
          red = RGBArray[i * 3];
          green = RGBArray[i * 3 + 1];
          blue = RGBArray[i * 3 + 2];
          this.context.fillStyle = "rgb(" + red + "," + green + "," + blue + ")";
          this.context.fillRect(i * (this.squareWidth + 1), 40, this.squareWidth, this.squareWidth);
          _results.push(this.context.fillRect(i * (this.squareWidth + 1), this.height - 40, this.squareWidth, this.squareWidth));
        }
        return _results;
      };

      return BemisPreview;

    })(Backbone.View);
  })();

}).call(this);
