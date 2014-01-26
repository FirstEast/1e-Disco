(function() {
  (function() {
    return com.firsteast.DiscoSession = (function() {
      function DiscoSession() {
        var device, _i, _j, _len, _len1, _ref, _ref1;
        this.beatModel = new com.firsteast.BeatModel();
        this.realDiscoModel = new com.firsteast.DiscoModel();
        this.mockDiscoModel = new com.firsteast.DiscoModel();
        this.patternList = new Backbone.Collection();
        this.patternList.model = com.firsteast.PatternModel;
        this.savedPatternList = new Backbone.Collection();
        this.savedPatternList.model = com.firsteast.PatternModel;
        this.outputDeviceModel = new Backbone.Model();
        _ref = com.firsteast.OUTPUT_DEVICES;
        for (_i = 0, _len = _ref.length; _i < _len; _i++) {
          device = _ref[_i];
          this.outputDeviceModel.set(device, false);
        }
        this.inputDeviceModel = new Backbone.Model();
        _ref1 = com.firsteast.INPUT_DEVICES;
        for (_j = 0, _len1 = _ref1.length; _j < _len1; _j++) {
          device = _ref1[_j];
          this.inputDeviceModel.set(device, false);
        }
        this.gifList = new Backbone.Collection();
      }

      return DiscoSession;

    })();
  })();

}).call(this);
