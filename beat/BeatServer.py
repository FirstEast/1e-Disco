from twisted.internet import reactor, task
from twisted.internet.endpoints import TCP4ClientEndpoint
from autobahn.twisted.websocket import listenWS
from sockets import AudioWebSocketFactory, AudioWebSocket, AudioSocketFactory
from sys import argv

from processAudio import *

from optparse import OptionParser

DISCO_SERVER_HOST = 'localhost'
DISCO_SERVER_PORT = 8347

WEB_SOCKET_PORT = 2000

parser = OptionParser()
parser.add_option("-d", "--disco", action="store", dest="host", default=DISCO_SERVER_HOST,\
                  help="Disco Server Host", metavar="HOSTNAME")
parser.add_option("-p", "--port", action="store", dest="port", default=DISCO_SERVER_PORT,\
                  help="Disco Server Port", metavar="PORT")
parser.add_option("-w", "--wave", action="store", dest="wavefile", default=None,\
                  help=".wav file for non-streaming")
parser.add_option("-i", "--input", action="store", dest="input", default=2,\
                  help="Input device index for audio")

if __name__ == '__main__':
  (options, args) = parser.parse_args()

  # Beat data model. Creates the model and stream, then repeatedly processes data
  if options.wavefile != None: 
    stream = WaveStream(options.wavefile) # for debugging purposes - MUST CALL 'python BeatServer.py wavemode <filename>'
  else: 
    stream = getAudioStream(options.input)

  audioProcessor = AudioProcessor(stream)
  
  task.LoopingCall(lambda: audioProcessor.processChunk()).start(0.01)

  # Start the audio serving websocket
  audioFactory = AudioWebSocketFactory("ws://localhost:" + str(WEB_SOCKET_PORT), audioProcessor, debug = False)
  audioFactory.protocol = AudioWebSocket
  listenWS(audioFactory)

  # Setup render socket
  point = TCP4ClientEndpoint(reactor, options.host, options.port)
  d = point.connect(AudioSocketFactory(audioProcessor))

  reactor.run()
