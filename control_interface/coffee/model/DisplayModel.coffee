do ->
  class com.firsteast.DisplayModel extends Backbone.Model
    defaults: =>
      attrs =
        showReal: true
        showMock: true
      
      for device in com.firsteast.OUTPUT_DEVICES
        attrs["show#{device}"] = true
