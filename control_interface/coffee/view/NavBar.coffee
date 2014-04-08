do ->
  class com.firsteast.NavBar extends Backbone.View
    initialize: (options) =>
      return

    render: =>
      @$el.empty()
      @$el.append com.firsteast.templates['nav-bar']()