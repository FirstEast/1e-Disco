do ->
  class com.firsteast.DiscoSession
    constructor: ->
      @beatModel = new com.firsteast.BeatModel()
      @realDiscoModel = new com.firsteast.DiscoModel()
      @mockDiscoModel = new com.firsteast.DiscoModel()
      @patternList = new Backbone.Collection()
      @patternList.model = com.firsteast.PatternModel

      @outputDeviceModel = new Backbone.Model()
      for device in com.firsteast.OUTPUT_DEVICES
        @outputDeviceModel[device] = false

      @inputDeviceModel = new Backbone.Model()
      for device in com.firsteast.INPUT_DEVICES
        @inputDeviceModel[device] = false
