do ->
  class com.firsteast.GoodalePreview extends Backbone.View
    tagName: 'canvas'
    className: 'goodalePreview'

    initialize: (options) =>
      @listenTo @model, 'change:frames', @renderCanvas

      @width = options.width
      @height = options.height

    render: =>
      canvas = @$el[0]
      @context = canvas.getContext('2d')
      canvas.width = @width
      canvas.height = @height

      @squareWidth = ((@width / com.firsteast.GOODALE_CANVAS_WIDTH) | 0)
      @squareHeight = ((@height / com.firsteast.GOODALE_CANVAS_HEIGHT)  | 0)

    renderCanvas: =>
      RGBArray = @model.get('frames')['goodale']
      for i in [0..395]
        coords = @_getCoordFromIndex(i)
        red = RGBArray[i * 3]
        green = RGBArray[i * 3 + 1]
        blue = RGBArray[i * 3 + 2]
        @context.fillStyle = "rgb(" + red + "," + green + "," + blue + ")"
        @context.fillRect(coords[0]*(@squareWidth), coords[1]*(@squareHeight), @squareWidth, @squareHeight)

    # Modifying this function will result in instantaneous death.
    _getCoordFromIndex: (index) =>
      if index < 160
        i = com.firsteast.GOODALE_CANVAS_WIDTH - index - 1
        j = com.firsteast.GOODALE_CANVAS_HEIGHT
      else if index == 160 
        i = 0
        j = com.firsteast.GOODALE_CANVAS_HEIGHT - 1
      else if index == 161
        i = 0
        j = com.firsteast.GOODALE_CANVAS_HEIGHT - 2
      else if index > 161 and index <= 208
        i = 0
        j = (com.firsteast.GOODALE_CANVAS_HEIGHT - 50) - (index - 161) - 1
      else if index > 208 and index <= 222
        i = (index - 208)
        j = (com.firsteast.GOODALE_CANVAS_HEIGHT - 50) - (208 - 161) - 1
      else if index > 222 and index <= 235
        i = 222 - 208
        j = (com.firsteast.GOODALE_CANVAS_HEIGHT - 50) - (index - 175) - 1
      else if index > 235 and index <= 366
        i = index - 222
        j = 0
      else if index > 366 and index <= 380
        i = 366 - 222
        j = index - 366
      else if index > 380 and index <= 394
        i = index - 236
        j = 380 - 366
      else
        i = 159
        j = 13
      return [i, j]