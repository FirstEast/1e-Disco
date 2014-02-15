do ->
  class com.firsteast.PreviewArea extends Backbone.View
    className: 'preview-area'

    initialize: (options) =>
      @session = options.session
      @model = options.model

      @selectors = {}
      for device in com.firsteast.OUTPUT_DEVICES
        selector = new com.firsteast.PatternSelector
          discoModel: @model
          patternList: @session.patternList
          savedPatternList: @session.savedPatternList
          gifList: @session.gifList
          imageList: @session.imageList
          device: device
        @selectors[device] = selector

    render: =>
      for key,view of @selectors
        view.render()
        @$el.append(view.$el)
