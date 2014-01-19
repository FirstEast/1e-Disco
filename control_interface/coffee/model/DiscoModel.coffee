do ->
  class com.firsteast.DiscoModel extends Backbone.Model
    defaults: =>
      attrs =
        frames: {}
        patterns: {}

      # Frame and pattern for each device
      for device in com.firsteast.OUTPUT_DEVICES
        attrs.frames[device] = []
        attrs.patterns[device] = null

      return attrs