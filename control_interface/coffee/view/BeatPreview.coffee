do ->
  class com.firsteast.BeatPreview extends Backbone.View
    className: 'beat-preview'

    initialize: (options) =>
      @model = options.model
      @$el.append('<div class="bar-container"/>')

      width = Math.floor(100 / 48) + '%'
      for i in [0..48]
        @$('.bar-container').append($('<div class="bar"/>').css('width', width));

      @listenTo @model, 'change', @render

    render: =>
      freqs = @model.get('frequencies')
      $bars = @$('.bar')
      for i in [0..freqs.length]
        $($bars[i]).css('height', ((Math.min((freqs[i] - 0.66)*3, 1))*100 + 1) + '%'); 