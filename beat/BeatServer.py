from twisted.internet import reactor, task
from twisted.internet.endpoints import TCP4ClientEndpoint
from autobahn.twisted.websocket import listenWS
from sockets import AudioWebSocketFactory, AudioWebSocket, AudioSocketFactory

import process_audio

DISCO_SERVER_HOST = 'localhost'
DISCO_SERVER_PORT = 8347

WEB_SOCKET_PORT = 2000

if __name__ == '__main__':
  # Beat data model. Creates the model and stream, then repeatedly processes data
  beatData = process_audio.BeatData()
  stream = process_audio.getAudioStream()
  task.LoopingCall(lambda: process_audio.processChunk(stream, beatData)).start(0.01)

  # Start the audio serving websocket
  audioFactory = AudioWebSocketFactory("ws://localhost:" + str(WEB_SOCKET_PORT), beatData, debug = False)
  audioFactory.protocol = AudioWebSocket
  listenWS(audioFactory)

  # Setup render socket
  point = TCP4ClientEndpoint(reactor, DISCO_SERVER_HOST, DISCO_SERVER_PORT)
  d = point.connect(AudioSocketFactory(beatData))

  reactor.run()