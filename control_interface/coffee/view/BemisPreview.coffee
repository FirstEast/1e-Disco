do ->
  class com.firsteast.BemisPreview extends Backbone.View
    tagName: 'canvas'
    className: 'bemisPreview'

    initialize: (options) =>
      @listenTo @model, 'change:frames', @renderCanvas

      @width = options.width
      @height = options.height

    render: =>
      canvas = @$el[0]
      @context = canvas.getContext('2d')
      canvas.width = @width
      canvas.height = @height

      @squareWidth = ((@width / com.firsteast.BEMIS_WIDTH) | 0)

    renderCanvas: =>
      RGBArray = @model.get('frames')['bemis']
      for i in [0..com.firsteast.BEMIS_WIDTH]
        red = RGBArray[i*3]
        green = RGBArray[i*3 + 1]
        blue = RGBArray[i*3 + 2]
        @context.fillStyle = "rgb(" + red + "," + green + "," + blue + ")"
        @context.fillRect(i*(@squareWidth), 40, @squareWidth, @squareWidth)
        @context.fillRect(i*(@squareWidth), @height-40, @squareWidth, @squareWidth)
