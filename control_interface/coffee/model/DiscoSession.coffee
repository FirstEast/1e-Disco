do ->
  class com.firsteast.DiscoSession
    constructor: ->
      @beatModel = new com.firsteast.BeatModel()
      @realDiscoModel = new com.firsteast.DiscoModel()
      @mockDiscoModel = new com.firsteast.DiscoModel()

      @patternList = new Backbone.Collection()
      @patternList.model = com.firsteast.PatternModel

      @savedPatternList = new Backbone.Collection()
      @savedPatternList.model = com.firsteast.PatternModel

      @outputDeviceModel = new Backbone.Model()
      for device in com.firsteast.OUTPUT_DEVICES
        @outputDeviceModel.set(device, false)

      @inputDeviceModel = new Backbone.Model()
      for device in com.firsteast.INPUT_DEVICES
        @inputDeviceModel.set(device, false)
