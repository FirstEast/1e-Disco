do ->
  class com.firsteast.DdfDebug extends Backbone.View
    className: 'ddfDebug'
    events:
      'change select': '_changeSelected'

    initialize: (options) =>
      @patternList = options.patternList
      @realDiscoModel = options.realDiscoModel

      @listenTo @patternList, 'reset', @render
      @listenTo @realDiscoModel, 'change:ddfPattern', @_updateSelected

    render: =>
      @$el.empty()
      source = $('#ddf-debug-template').html()
      template = Handlebars.compile(source)
      @$el.append template({patterns: @patternList.models})
      @_updateSelected()

    _updateSelected: =>
      @$('select').val(@realDiscoModel.get('ddfPattern')?.get('name'))

    _changeSelected: =>
      name = @$('select').val()
      pattern = @patternList.where({name: name})[0].attributes
      pattern = $.extend(true, {}, pattern)
      @realDiscoModel.set('ddfPattern', new com.firsteast.PatternModel(pattern))