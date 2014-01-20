(function() {
  var __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; },
    __hasProp = {}.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; };

  (function() {
    var _ref;
    return com.firsteast.DdfDebug = (function(_super) {
      __extends(DdfDebug, _super);

      function DdfDebug() {
        this._changeSelected = __bind(this._changeSelected, this);
        this._updateSelected = __bind(this._updateSelected, this);
        this.render = __bind(this.render, this);
        this.initialize = __bind(this.initialize, this);
        _ref = DdfDebug.__super__.constructor.apply(this, arguments);
        return _ref;
      }

      DdfDebug.prototype.className = 'ddfDebug';

      DdfDebug.prototype.events = {
        'change select': '_changeSelected'
      };

      DdfDebug.prototype.initialize = function(options) {
        this.patternList = options.patternList;
        this.realDiscoModel = options.realDiscoModel;
        this.listenTo(this.patternList, 'reset', this.render);
        return this.listenTo(this.realDiscoModel, 'change:patterns', this._updateSelected);
      };

      DdfDebug.prototype.render = function() {
        var source, template;
        this.$el.empty();
        source = $('#ddf-debug-template').html();
        template = Handlebars.compile(source);
        this.$el.append(template({
          patterns: this.patternList.models
        }));
        return this._updateSelected();
      };

      DdfDebug.prototype._updateSelected = function() {
        var _ref1;
        return this.$('select').val((_ref1 = this.realDiscoModel.get('patterns').ddf) != null ? _ref1.get('name') : void 0);
      };

      DdfDebug.prototype._changeSelected = function() {
        var name, pattern, realPatterns;
        name = this.$('select').val();
        pattern = this.patternList.where({
          name: name
        })[0].attributes;
        pattern = $.extend(true, {}, pattern);
        realPatterns = $.extend(true, {}, this.realDiscoModel.get('patterns'));
        realPatterns['ddf'] = new com.firsteast.PatternModel(pattern);
        return this.realDiscoModel.set('patterns', realPatterns);
      };

      return DdfDebug;

    })(Backbone.View);
  })();

}).call(this);
