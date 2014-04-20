do ->
  class com.firsteast.DisplayModel extends Backbone.Model
    defaults: =>
      attrs =
        showReal: true
        showMock: false
      
      for device in com.firsteast.OUTPUT_DEVICES
        attrs["show#{device}"] = true
      return attrs