do ->
  PREVIEW_VIEWS = {}

  PREVIEW_VIEWS['ddf'] = class com.firsteast.DdfPreview extends Backbone.View
    tagName: 'canvas'
    className: 'ddfPreview'

    initialize: (options) =>
      @listenTo @model, 'change:frames', @renderCanvas

      @width = com.firsteast.DDF_WIDTH*8
      @height = com.firsteast.DDF_HEIGHT*8

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

  PREVIEW_VIEWS['goodale'] = class com.firsteast.GoodalePreview extends Backbone.View
    tagName: 'canvas'
    className: 'goodalePreview'

    initialize: (options) =>
      @listenTo @model, 'change:frames', @renderCanvas

      @width = com.firsteast.GOODALE_CANVAS_WIDTH*3
      @height = 111*3

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

  PREVIEW_VIEWS['bemis'] = class com.firsteast.BemisPreview extends Backbone.View
    tagName: 'canvas'
    className: 'bemisPreview'

    initialize: (options) =>
      @listenTo @model, 'change:frames', @renderCanvas

      @width = com.firsteast.BEMIS_WIDTH
      @height = 24*6

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


  class com.firsteast.DevicePreview extends Backbone.View
    initialize: (options) =>
      @internalView = new PREVIEW_VIEWS[options.device]
        model: options.model

    render: =>
      @internalView.render()
      @$el.html(@internalView.$el)
