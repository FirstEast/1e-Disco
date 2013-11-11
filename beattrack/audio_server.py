from twisted.internet import reactor, task
from twisted.web.server import Site
from twisted.web.static import File
from autobahn.websocket import listenWS, WebSocketServerProtocol, \
                                WebSocketServerFactory

import pyaudio
import json
import numpy as np
import sys, os

WEB_SOCKET_PORT = 2000
INTERFACE_PORT = 90
INTERFACE_DIR = "interface"

class AudioWebSocket(WebSocketServerProtocol):
  def onOpen(self):
    self.factory.register(self)

  def connectionLost(self, reason):
    WebSocketServerProtocol.connectionLost(self, reason)
    self.factory.unregister(self)

class AudioWebSocketFactory(WebSocketServerFactory):
  def __init__(self, url, debug = False, debugCodePaths = False):
    WebSocketServerFactory.__init__(self, url, debug = debug, debugCodePaths = debugCodePaths)
    self.clients = []

    self.stream = startListening()

    task.LoopingCall(self.sendData).start(0.01)

  def sendData(self):
    vals = fetchData(self.stream)
    self.broadcast(json.dumps(vals))

  def register(self, client):
    if not client in self.clients:
      self.clients.append(client)

  def unregister(self, client):
    if client in self.clients:
      self.clients.remove(client)

  def broadcast(self, msg):
    for c in self.clients:
      c.sendMessage(msg)


CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100

MIN_FREQ = 30 #Hz
MAX_FREQ = 20000 #Hz
SCALE = 2
BUCKETS = 20

BANDS = [
  [20, 140],
  [140, 400],
  [400, 2600],
  [2600, 5200],
  [5200, 20000]
]

FREQ_PER_BUCKET = int((MAX_FREQ - MIN_FREQ) / BUCKETS)

def startListening():
  p = pyaudio.PyAudio()
  stream = p.open(format = FORMAT,
                  channels = CHANNELS,
                  rate = RATE,
                  input = True,
                  output=True,
                  frames_per_buffer = CHUNK)
  return stream

def fetchData(stream):
  new_data = stream.read(CHUNK)
  stream.write(new_data, CHUNK)
  rfft = np.fft.rfft([ord(i) for i in new_data])

  result = []
  for i in range(BUCKETS):
    freq_range = [MIN_FREQ + i * FREQ_PER_BUCKET, MIN_FREQ + (i + 1) * FREQ_PER_BUCKET]
  # for band in BANDS:
  #   freq_range = band
  # lower = MIN_FREQ
  # upper = 2 * MIN_FREQ
  # while lower < MAX_FREQ:
  #   freq_range = [lower, upper]
    freq_cutoffs = np.array(freq_range)
    fft_cutoffs = freq_cutoffs * 1024/RATE
    val = sum([abs(j) for j in rfft[fft_cutoffs[0]:fft_cutoffs[1]]])
    if val < 0:
      val = 0
    result.append(int(val))

    # lower = upper
    # upper = 2*upper

  return result

if __name__ == '__main__':
  # Start the audio serving websocket
  audioFactory = AudioWebSocketFactory("ws://localhost:" + str(WEB_SOCKET_PORT), debug = False)
  audioFactory.protocol = AudioWebSocket
  listenWS(audioFactory)

  # Setup static html serving
  resource = File(INTERFACE_DIR)
  staticServerFactory = Site(resource)
  reactor.listenTCP(INTERFACE_PORT, staticServerFactory)

  reactor.run()