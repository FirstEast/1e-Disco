(function() {
  var __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; },
    __hasProp = {}.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; };

  (function() {
    var _ref;
    return com.firsteast.GoodalePreview = (function(_super) {
      __extends(GoodalePreview, _super);

      function GoodalePreview() {
        this._getCoordFromIndex = __bind(this._getCoordFromIndex, this);
        this.renderCanvas = __bind(this.renderCanvas, this);
        this.render = __bind(this.render, this);
        this.initialize = __bind(this.initialize, this);
        _ref = GoodalePreview.__super__.constructor.apply(this, arguments);
        return _ref;
      }

      GoodalePreview.prototype.tagName = 'canvas';

      GoodalePreview.prototype.className = 'goodalePreview';

      GoodalePreview.prototype.initialize = function(options) {
        this.listenTo(this.model, 'change:frames', this.renderCanvas);
        this.width = options.width;
        return this.height = options.height;
      };

      GoodalePreview.prototype.render = function() {
        var canvas;
        canvas = this.$el[0];
        this.context = canvas.getContext('2d');
        canvas.width = this.width;
        canvas.height = this.height;
        this.squareWidth = (this.width / com.firsteast.GOODALE_CANVAS_WIDTH) | 0;
        return this.squareHeight = (this.height / com.firsteast.GOODALE_CANVAS_HEIGHT) | 0;
      };

      GoodalePreview.prototype.renderCanvas = function() {
        var RGBArray, blue, coords, green, i, red, _i, _results;
        RGBArray = this.model.get('frames')['goodale'];
        _results = [];
        for (i = _i = 0; _i <= 395; i = ++_i) {
          coords = this._getCoordFromIndex(i);
          red = RGBArray[i * 3];
          green = RGBArray[i * 3 + 1];
          blue = RGBArray[i * 3 + 2];
          this.context.fillStyle = "rgb(" + red + "," + green + "," + blue + ")";
          _results.push(this.context.fillRect(coords[0] * this.squareWidth, coords[1] * this.squareHeight, this.squareWidth, this.squareHeight));
        }
        return _results;
      };

      GoodalePreview.prototype._getCoordFromIndex = function(index) {
        var i, j;
        if (index < 160) {
          i = com.firsteast.GOODALE_CANVAS_WIDTH - index - 1;
          j = com.firsteast.GOODALE_CANVAS_HEIGHT;
        } else if (index === 160) {
          i = 0;
          j = com.firsteast.GOODALE_CANVAS_HEIGHT - 1;
        } else if (index === 161) {
          i = 0;
          j = com.firsteast.GOODALE_CANVAS_HEIGHT - 2;
        } else if (index > 161 && index <= 208) {
          i = 0;
          j = (com.firsteast.GOODALE_CANVAS_HEIGHT - 50) - (index - 161) - 1;
        } else if (index > 208 && index <= 222) {
          i = index - 208;
          j = (com.firsteast.GOODALE_CANVAS_HEIGHT - 50) - (208 - 161) - 1;
        } else if (index > 222 && index <= 235) {
          i = 222 - 208;
          j = (com.firsteast.GOODALE_CANVAS_HEIGHT - 50) - (index - 175) - 1;
        } else if (index > 235 && index <= 366) {
          i = index - 222;
          j = 0;
        } else if (index > 366 && index <= 380) {
          i = 366 - 222;
          j = index - 366;
        } else if (index > 380 && index <= 394) {
          i = index - 236;
          j = 380 - 366;
        } else {
          i = 159;
          j = 13;
        }
        return [i, j];
      };

      return GoodalePreview;

    })(Backbone.View);
  })();

}).call(this);
