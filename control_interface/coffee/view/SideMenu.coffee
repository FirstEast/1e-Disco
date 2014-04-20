do ->
  class com.firsteast.SideMenu extends Backbone.View
    events:
      'click .swap-mock-real':'_triggerMockToRealSwap'
      'click .swap-real-mock':'_triggerRealToMockSwap'
      'change .show-real': '_toggleShowReal'
      'change .show-mock': '_toggleShowMock'
      'click .handle': '_toggleShowing'
      'change .hotkey-patterns': '_changeHotkeyPattern'

    initialize: (options) =>
      @model = options.model
      @realDiscoModel = options.realDiscoModel
      @mockDiscoModel = options.mockDiscoModel
      @savedPatternList = options.savedPatternList
      @hotkeyModel = options.hotkeyModel

      @showing = true

      @listenTo @savedPatternList, 'add remove reset', @render
      @listenTo @hotkeyModel, 'change:shownDevice', @render

    render: =>
      @$el.empty()
      template = com.firsteast.templates['side-menu']

      saveModels = _.sortBy(@savedPatternList.filter((x) => x.get('DEVICES').indexOf(@hotkeyModel.get('shownDevice')) >= 0), (x) -> return x.get('saveName'))
      col = new Backbone.Collection(saveModels)
      partyWorthySaveModels = col.where({partyWorthy: true})
      nonPartyWorthySaveModels = col.where({partyWorthy: false})

      @hotkeySet = @hotkeyModel.get('hotkeyPatterns')[@hotkeyModel.get('shownDevice')]

      @$el.append(template({
        displayAttrs: @model.attributes
        partyWorthySaveModels: partyWorthySaveModels
        nonPartyWorthySaveModels: nonPartyWorthySaveModels
        hotkeySet: @hotkeySet
      }))

      @_updateSelectedHotkeyPatterns()

    _updateSelectedHotkeyPatterns: =>
      for el in @$('.hotkey-patterns')
        key = $(el).data().key
        $(el).val(@hotkeySet[key])

    _changeHotkeyPattern: (event) =>
      key = @$(event.target).data().key
      @hotkeySet[key] = @$(event.target).val()
      fullSet = @hotkeyModel.get('hotkeyPatterns')
      fullSet[@hotkeyModel.get('shownDevice')] = @hotkeySet
      @hotkeyModel.set('hotkeyPatterns', fullSet)

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
