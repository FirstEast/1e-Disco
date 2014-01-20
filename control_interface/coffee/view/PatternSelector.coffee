do ->
  class com.firsteast.PatternSelector extends Backbone.View
    className: 'patternSelector'
    events:
      'change select': '_changeSelected'

    initialize: (options) =>
      @patternList = options.patternList
      @discoModel = options.discoModel
      @device  = options.device

      @listenTo @patternList, 'reset', @render
      @listenTo @discoModel, "change:#{@device}Pattern", @_updateSelected

    render: =>
      @$el.empty()
      source = $('#ddf-debug-template').html()
      template = Handlebars.compile(source)
      models = @patternList.filter(((x) => x.get('DEVICES').indexOf(@device) >= 0))
      @$el.append template({patterns: models})
      @_updateSelected()

    _updateSelected: =>
      @$('select').val(@discoModel.get("#{@device}Pattern")?.get('name'))

    _changeSelected: =>
      name = @$('select').val()
      pattern = @patternList.where({name: name})[0].attributes
      pattern = $.extend(true, {}, pattern)
      @discoModel.set("#{@device}Pattern", new com.firsteast.PatternModel(pattern))