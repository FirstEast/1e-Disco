do ->
  class com.firsteast.BeatModel extends Backbone.Model
    defaults: =>
      centroid: 0
      volume: 0
      frequencies: []