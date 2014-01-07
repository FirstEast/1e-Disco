do ->
  class com.firsteast.PatternModel extends Backbone.Model
    defaults: =>
      # Module of the python class on the server
      __module__: null

      # Configuration stuff about the pattern
      USE_BEAT: false
      DEVICES: []
      DEFAULT_PARAMS: []

      # Actual pattern settings
      params: []