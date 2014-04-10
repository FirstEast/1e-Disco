do ->
  class com.firsteast.PatternSelector extends Backbone.View
    className: 'pattern-selector'
    events:
      'change .class-patterns': '_changeClassSelected'
      'change .saved-patterns': '_changeSavedSelected'
      'change .param-input': '_changeParams'
      'click .save-button': '_savePattern'
      'click .expander': '_toggleShowEdit'

    initialize: (options) =>
      @patternList = options.patternList
      @savedPatternList = options.savedPatternList
      @discoModel = options.discoModel
      @gifList = options.gifList
      @imageList = options.imageList
      @device  = options.device
      @isMock = options.isMock

      @previewView = new com.firsteast.DevicePreview
        device: @device
        model: @discoModel
      @previewView.render()

      @showEdit = false;
      @parameters = {}

      @listenTo @patternList, 'add remove reset', @render
      @listenTo @savedPatternList, 'add remove reset', @render
      @listenTo @discoModel, "change:#{@device}Pattern", @render
      @listenTo @gifList, 'add remove reset', @render
      @listenTo @imageList, 'add remove reset', @render

    render: =>
      @$el.empty()
      template = com.firsteast.templates['device-preview']

      models = _.sortBy(@patternList.filter(((x) => x.get('DEVICES').indexOf(@device) >= 0)), (x) -> return x.get('name'))
      saveModels = _.sortBy(@savedPatternList.filter((x) => x.get('DEVICES').indexOf(@device) >= 0), (x) -> return x.get('saveName'))
      partyWorthySaveModels = _.sortBy(@savedPatternList.where({partyWorthy: true}), (x) -> return x.name)
      nonPartyWorthySaveModels = _.sortBy(@savedPatternList.where({partyWorthy: false}), (x) -> return x.name)
      currentPattern = @discoModel.get("#{@device}Pattern")?.attributes
      parameters = @_parseParams(_.defaults({}, currentPattern?.params, currentPattern?.DEFAULT_PARAMS))

      @$el.append template({
        device: @device
        patterns: models
        savedPatterns: saveModels
        partyWorthySavedPatterns: partyWorthySaveModels
        nonPartyWorthySavedPatterns: nonPartyWorthySaveModels
        currentPattern: currentPattern
        gifList: @gifList.models
        imageList: @imageList.models
        parameters: parameters
        showEdit: @showEdit
        isMock: @isMock
      })

      @$('.preview-view').append(@previewView.$el)

      @_updateSelected()
      @_setParamValues(parameters)

    _parseParams: (params) =>
      result = []
      for key, val of params
        param = {name: key}
        param.val = val
        if typeof val == "object"
          if val.RGBValues?
            param.type = 'color'
            param.val = getHexStringFromRgb(param.val.RGBValues)
        else if typeof val == "boolean"
          param.type = 'checkbox'
        else if typeof val == "string"
          if val.indexOf('.json') >= 0
            param.pattern = true
            param.val = param.val.split('.json')[0]
          else if val.indexOf('.gif') >= 0
            param.gif = true
          else if val.indexOf('.jpg') >= 0 or val.indexOf('.png') >= 0
            param.image = true
          else
            param.type = 'text'
        else if typeof val == 'number' or !isNaN(val)
          param.type = 'number'
        else
          param.type = 'text'
        result.push(param)
      return _.sortBy(result, (x) -> return x.name)

    _setParamValues: (params) =>
      for param in params
        @$("[name='#{param.name}']").val(param.val)

    _toggleShowEdit: =>
      @showEdit = !@showEdit
      @render()

    _updateSelected: =>
      if @discoModel.get("#{@device}Pattern")?.get('saved')
        @$('select').val(@discoModel.get("#{@device}Pattern")?.get('saveName'))
      else
        @$('select').val(@discoModel.get("#{@device}Pattern")?.get('name'))

    _changeClassSelected: =>
      name = @$('.class-patterns').val()
      pattern = @patternList.where({name: name})[0].attributes
      pattern = $.extend(true, {}, pattern)
      @discoModel.set("#{@device}Pattern", new com.firsteast.PatternModel(pattern))

    _changeSavedSelected: =>
      name = @$('.saved-patterns').val()
      pattern = @savedPatternList.where({saveName: name})[0].attributes
      pattern = $.extend(true, {}, pattern)
      @discoModel.set("#{@device}Pattern", new com.firsteast.PatternModel(pattern))

    _changeParams: =>
      params = {}
      for input in @$('.param-input')
        inp = $(input)

        if inp.prop('type') == 'color'
          params[inp.prop('name')] = {RGBValues: getRgbFromHexString(inp.val())}
        else if inp.prop('type') == 'checkbox'
          params[inp.prop('name')] = inp.prop('checked')
        else if inp.data('type') == 'pattern'
          params[inp.prop('name')] = inp.val() + '.json'
        else if inp.prop('type') == 'number'
          params[inp.prop('name')] = parseFloat(inp.val())
        else
          params[inp.prop('name')] = inp.val()

      # HACK - recreates pattern, doesn't smoothly update params
      pattern = @discoModel.get("#{@device}Pattern").attributes
      pattern = $.extend(true, {}, pattern)
      pattern.params = params
      @discoModel.set("#{@device}Pattern", new com.firsteast.PatternModel(pattern))

    _savePattern: =>
      saveName = @$('.save-name-input').val()
      pattern = @discoModel.get("#{@device}Pattern").attributes
      pattern = $.extend(true, {}, pattern)
      pattern.saved = true
      pattern.saveName = saveName
      pattern.partyWorthy = @$('.party-worthy-input').prop('checked')
      patternModel = new com.firsteast.PatternModel(pattern)
      @savedPatternList.add(patternModel)

  getRgbFromHexString = (hex) =>
    red = parseInt(hex.substring(1,3), 16)
    green = parseInt(hex.substring(3,5), 16)
    blue = parseInt(hex.substring(5,7), 16)
    return [red, green, blue]

  getHexStringFromRgb = (RGB) =>
    total = "#"
    for val in RGB
      hex = val.toString(16)
      if hex.length == 1
        hex = '0' + hex
      total = total + hex
    return total