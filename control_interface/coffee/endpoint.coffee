com.firsteast.WEBSOCKET_URL = window.location.origin.split('//')[1].split(':')[0]
com.firsteast.WEBSOCKET_PORT = '9000'

com.firsteast.OUTPUT_DEVICES = ['goodale', 'bemis', 'ddf']
com.firsteast.INPUT_DEVICES = ['beat']

$('document').ready ( =>
  # Create the DiscoSession
  session = new com.firsteast.DiscoSession()

  # Create the controller that starts the websocket connection

  # Draw the main view
)