com.firsteast.WEBSOCKET_URL = window.location.origin.split('//')[1].split(':')[0]
com.firsteast.WEBSOCKET_PORT = '9000'

com.firsteast.OUTPUT_DEVICES = ['ddf', 'goodale', 'bemis']
com.firsteast.INPUT_DEVICES = ['beat']

com.firsteast.DDF_WIDTH = 48
com.firsteast.DDF_HEIGHT = 24

com.firsteast.BEMIS_WIDTH = 264

com.firsteast.GOODALE_CANVAS_WIDTH = 160
com.firsteast.GOODALE_CANVAS_HEIGHT = 110
com.firsteast.GOODALE_WIDTH = 395

$('document').ready ( =>
  # Create the DiscoSession
  session = new com.firsteast.DiscoSession()

  # Create the controller that starts the websocket connection
  controller = new com.firsteast.DiscoController
    session: session

  # Create our preview views
  for model in [session.realDiscoModel, session.mockDiscoModel]
    previewArea = new com.firsteast.PreviewArea
      model: model
      session: session
    previewArea.render()
    $('.previews').append(previewArea.$el)

  # Create the menu view
  sideMenu = new com.firsteast.SideMenu
    el: $('.menu')
    model: session.displayModel
    realDiscoModel: session.realDiscoModel
    mockDiscoModel: session.mockDiscoModel
  sideMenu.render()
)