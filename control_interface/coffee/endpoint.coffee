com.firsteast.WEBSOCKET_URL = window.location.origin.split('//')[1].split(':')[0]
com.firsteast.WEBSOCKET_PORT = '9000'

com.firsteast.OUTPUT_DEVICES = ['ddf', 'goodale', 'bemis']
com.firsteast.INPUT_DEVICES = ['beat']

com.firsteast.DDF_WIDTH = 16
com.firsteast.DDF_HEIGHT = 12

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
    width: com.firsteast.DDF_WIDTH*8
    height: com.firsteast.DDF_HEIGHT*8
  ddfPreview.render()

  goodalePreview = new com.firsteast.GoodalePreview
    model: session.realDiscoModel
    width: 160*3
    height: 111*3
  goodalePreview.render()

  bemisPreview = new com.firsteast.BemisPreview
    model: session.realDiscoModel
    width: 261*2
    height: 24*8
  bemisPreview.render()

  $('.realVis').append(ddfPreview.$el)
  $('.realVis').append(goodalePreview.$el)
  $('.realVis').append(bemisPreview.$el)

  for device in com.firsteast.OUTPUT_DEVICES
    selector = new com.firsteast.PatternSelector
      discoModel: session.realDiscoModel
      patternList: session.patternList
      savedPatternList: session.savedPatternList
      gifList: session.gifList
      imageList: session.imageList
      device: device
    selector.render()
    $('body').append(selector.$el)
)