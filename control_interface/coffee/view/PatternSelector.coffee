do ->
  class com.firsteast.PatternSelector extends Backbone.View
    className: 'patternSelector'
    events:
      'change .class-patterns': '_changeClassSelected'
      'change .saved-patterns': '_changeSavedSelected'
      'change .param-input': '_changeParams'
      'click .save-button': '_savePattern'

    initialize: (options) =>
      @patternList = options.patternList
      @savedPatternList = options.savedPatternList
      @discoModel = options.discoModel
      @device  = options.device

      @parameters = {}

      @listenTo @patternList, 'reset', @render
      @listenTo @savedPatternList, 'reset', @render
      @listenTo @discoModel, "change:#{@device}Pattern", @render

    render: =>
      @$el.empty()
      source = $('#ddf-debug-template').html()
      template = Handlebars.compile(source)
      models = @patternList.filter(((x) => x.get('DEVICES').indexOf(@device) >= 0))
      saveModels = @savedPatternList.filter((x) => x.get('DEVICES').indexOf(@device) >= 0)
      currentPattern = @discoModel.get("#{@device}Pattern")?.attributes
      parameters = @_parseParams(_.defaults({}, currentPattern?.params, currentPattern?.DEFAULT_PARAMS))
      @$el.append template({
        device: @device
        patterns: models
        savedPatterns: saveModels
        currentPattern: currentPattern
        parameters: parameters
      })
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
      return result

    _setParamValues: (params) =>
      for param in params
        @$("[name='#{param.name}']").val(param.val)

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

      # HACK
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