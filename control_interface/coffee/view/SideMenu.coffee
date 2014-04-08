do ->
  class com.firsteast.SideMenu extends Backbone.View
    events:
      'click .swap-mock-real':'_triggerMockToRealSwap'
      'click .swap-real-mock':'_triggerRealToMockSwap'
      'change .show-real': '_toggleShowReal'
      'change .show-mock': '_toggleShowMock'
      'click .handle': '_toggleShowing'

    initialize: (options) =>
      @model = options.model
      @realDiscoModel = options.realDiscoModel
      @mockDiscoModel = options.mockDiscoModel
      @showing = true;

    render: =>
      @$el.empty()
      template = com.firsteast.templates['side-menu']
      @$el.append(template(@model.attributes))

    _triggerMockToRealSwap: =>
      for device in com.firsteast.OUTPUT_DEVICES
        attributes = @mockDiscoModel.get("#{device}Pattern").attributes
        @realDiscoModel.set("#{device}Pattern", new com.firsteast.PatternModel($.extend(true, {}, attributes)))

    _triggerRealToMockSwap: =>
      for device in com.firsteast.OUTPUT_DEVICES
        attributes = @realDiscoModel.get("#{device}Pattern").attributes
        @mockDiscoModel.set("#{device}Pattern", new com.firsteast.PatternModel($.extend(true, {}, attributes)))

    _toggleShowReal: =>
      @model.set 'showReal', @$('.show-real').prop('checked')

    _toggleShowMock: =>
      @model.set 'showMock', @$('.show-mock').prop('checked')

    _toggleShowing: =>
      if @showing
        @$('.controls').hide()
        @$el.addClass('hiding')
      else
        setTimeout((() => @$('.controls').show()), 500)
        @$el.removeClass('hiding')

      @showing = !@showing
