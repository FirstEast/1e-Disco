do ->
  class com.firsteast.SideMenu extends Backbone.View
    events:
      'click .swap-mock-real':'_triggerMockToRealSwap'
      'click .swap-real-mock':'_triggerRealToMockSwap'

    initialize: (options) =>
      @model = options.model
      @realDiscoModel = options.realDiscoModel
      @mockDiscoModel = options.mockDiscoModel

    render: =>
      @$el.empty()
      source = $('#side-menu-template').html()
      template = Handlebars.compile(source)
      @$el.append(template(@model.attributes))

    _triggerMockToRealSwap: =>
      for device in com.firsteast.OUTPUT_DEVICES
        attributes = @mockDiscoModel.get("#{device}Pattern").attributes
        @realDiscoModel.set("#{device}Pattern", new com.firsteast.PatternModel($.extend(true, {}, attributes)))

    _triggerRealToMockSwap: =>
      for device in com.firsteast.OUTPUT_DEVICES
        attributes = @realDiscoModel.get("#{device}Pattern").attributes
        @mockDiscoModel.set("#{device}Pattern", new com.firsteast.PatternModel($.extend(true, {}, attributes)))