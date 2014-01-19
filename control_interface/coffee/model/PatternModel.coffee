do ->
  class com.firsteast.PatternModel extends Backbone.Model
    defaults: =>
      # Module of the python class on the server
      __module__: null

      # Name of the python class on the server
      name: null

      # Configuration stuff about the pattern
      USE_BEAT: false
      DEVICES: com.firsteast.OUTPUT_DEVICES
      DEFAULT_PARAMS: {}

      # Actual pattern settings
      params: {}