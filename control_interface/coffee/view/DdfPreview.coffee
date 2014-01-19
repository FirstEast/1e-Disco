do ->
  class com.firsteast.DdfPreview extends Backbone.View
    tagName: 'canvas'
    className: 'ddfPreview'

    initialize: (options) =>
      @listenTo @model, 'change:frames', @renderCanvas

      @width = options.width
      @height = options.height

    render: =>
      canvas = @$el[0]
      @context = canvas.getContext('2d')
      canvas.width = @width
      canvas.height = @height

      @squareWidth = ((@width / com.firsteast.DDF_WIDTH) | 0) - 1

    renderCanvas: =>
      RGBArray = @model.get('frames')['ddf']
      for i in [0..com.firsteast.DDF_HEIGHT]
        for j in [0..com.firsteast.DDF_WIDTH]
          red = RGBArray[(i * com.firsteast.DDF_WIDTH + j)*3]
          green = RGBArray[(i * com.firsteast.DDF_WIDTH + j)*3 + 1]
          blue = RGBArray[(i * com.firsteast.DDF_WIDTH + j)*3 + 2]
          @context.fillStyle = "rgb(" + red + "," + green + "," + blue + ")"
          @context.fillRect(j*(@squareWidth + 1), i*(@squareWidth + 1), @squareWidth, @squareWidth)
