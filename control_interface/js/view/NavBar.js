(function() {
  var __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; },
    __hasProp = {}.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; };

  (function() {
    return com.firsteast.NavBar = (function(_super) {
      __extends(NavBar, _super);

      function NavBar() {
        this.render = __bind(this.render, this);
        this.initialize = __bind(this.initialize, this);
        return NavBar.__super__.constructor.apply(this, arguments);
      }

      NavBar.prototype.initialize = function(options) {};

      NavBar.prototype.render = function() {
        this.$el.empty();
        return this.$el.append(com.firsteast.templates['nav-bar']());
      };

      return NavBar;

    })(Backbone.View);
  })();

}).call(this);
