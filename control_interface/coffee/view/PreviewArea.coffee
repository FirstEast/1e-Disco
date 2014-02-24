do ->
  class com.firsteast.PreviewArea extends Backbone.View
    className: 'preview-area'

    initialize: (options) =>
      @session = options.session
      @model = options.model
      @isMock = options.isMock
      @displayModel = @session.displayModel

      @selectors = {}
      for device in com.firsteast.OUTPUT_DEVICES
        selector = new com.firsteast.PatternSelector
          discoModel: @model
          patternList: @session.patternList
          savedPatternList: @session.savedPatternList
          gifList: @session.gifList
          imageList: @session.imageList
          device: device
          isMock: @isMock
        @selectors[device] = selector

      if @isMock
        @listenTo @displayModel, 'change:showMock', @render
      else
        @listenTo @displayModel, 'change:showReal', @render

    render: =>
      for key,view of @selectors
        view.render()
        @$el.append(view.$el)

      if @isMock && !@displayModel.get('showMock')
        @$el.hide()
      else if !@isMock && !@displayModel.get('showReal')
        @$el.hide()
      else
        @$el.show()