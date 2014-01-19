com.firsteast.WEBSOCKET_URL = window.location.origin.split('//')[1].split(':')[0]
com.firsteast.WEBSOCKET_PORT = '9000'

com.firsteast.OUTPUT_DEVICES = ['goodale', 'bemis', 'ddf']
com.firsteast.INPUT_DEVICES = ['beat']

com.firsteast.DDF_WIDTH = 48
com.firsteast.DDF_HEIGHT = 24

com.firsteast.BEMIS_WIDTH = 261

com.firsteast.GOODALE_CANVAS_WIDTH = 160
com.firsteast.GOODALE_CANVAS_HEIGHT = 110
com.firsteast.GOODALE_WIDTH = 395

$('document').ready ( =>
  # Create the DiscoSession
  session = new com.firsteast.DiscoSession()

  # Create the controller that starts the websocket connection
  controller = new com.firsteast.DiscoController
    session: session

  # Draw the main view
  # TODO: actually make a UI

  # Draw some debug views
  ddfPreview = new com.firsteast.DdfPreview
    model: session.realDiscoModel
    width: 48*8
    height: 24*8
  ddfPreview.render()

  bemisPreview = new com.firsteast.BemisPreview
    model: session.realDiscoModel
    width: 261*3
    height: 24*8
  bemisPreview.render()

  goodalePreview = new com.firsteast.GoodalePreview
    model: session.realDiscoModel
    width: 160*3
    height: 111*3
  goodalePreview.render()

  $('body').append(ddfPreview.$el)
  $('body').append(bemisPreview.$el)
  $('body').append(goodalePreview.$el)
)