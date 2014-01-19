(function() {
  var __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; },
    __hasProp = {}.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; };

  (function() {
    var _ref;
    return com.firsteast.DdfPreview = (function(_super) {
      __extends(DdfPreview, _super);

      function DdfPreview() {
        this.renderCanvas = __bind(this.renderCanvas, this);
        this.render = __bind(this.render, this);
        this.initialize = __bind(this.initialize, this);
        _ref = DdfPreview.__super__.constructor.apply(this, arguments);
        return _ref;
      }

      DdfPreview.prototype.tagName = 'canvas';

      DdfPreview.prototype.className = 'ddfPreview';

      DdfPreview.prototype.initialize = function(options) {
        this.listenTo(this.model, 'change:frames', this.renderCanvas);
        this.width = options.width;
        return this.height = options.height;
      };

      DdfPreview.prototype.render = function() {
        var canvas;
        canvas = this.$el[0];
        this.context = canvas.getContext('2d');
        canvas.width = this.width;
        canvas.height = this.height;
        return this.squareWidth = ((this.width / com.firsteast.DDF_WIDTH) | 0) - 1;
      };

      DdfPreview.prototype.renderCanvas = function() {
        var RGBArray, blue, green, i, j, red, _i, _ref1, _results;
        RGBArray = this.model.get('frames')['ddf'];
        _results = [];
        for (i = _i = 0, _ref1 = com.firsteast.DDF_HEIGHT; 0 <= _ref1 ? _i <= _ref1 : _i >= _ref1; i = 0 <= _ref1 ? ++_i : --_i) {
          _results.push((function() {
            var _j, _ref2, _results1;
            _results1 = [];
            for (j = _j = 0, _ref2 = com.firsteast.DDF_WIDTH; 0 <= _ref2 ? _j <= _ref2 : _j >= _ref2; j = 0 <= _ref2 ? ++_j : --_j) {
              red = RGBArray[(i * com.firsteast.DDF_WIDTH + j) * 3];
              green = RGBArray[(i * com.firsteast.DDF_WIDTH + j) * 3 + 1];
              blue = RGBArray[(i * com.firsteast.DDF_WIDTH + j) * 3 + 2];
              this.context.fillStyle = "rgb(" + red + "," + green + "," + blue + ")";
              _results1.push(this.context.fillRect(j * (this.squareWidth + 1), i * (this.squareWidth + 1), this.squareWidth, this.squareWidth));
            }
            return _results1;
          }).call(this));
        }
        return _results;
      };

      return DdfPreview;

    })(Backbone.View);
  })();

}).call(this);
