from twisted.internet.protocol import Protocol, ReconnectingClientFactory

import json
import time
import struct

WIDTH = 48
HEIGHT = 24

class RenderSocket(Protocol):
  def __init__(self, visualizeFactory):
    self.visualizeFactory = visualizeFactory
    self.frame = 0

    self.lastData = ''

  def connectionMade(self):
    print "connected successfully to central server"

    time.sleep(1)

    # Signal for the next frame
    self.sendMessage("OK")

  def dataReceived(self, line):
    line = self.lastData + line.strip()

    # Parse what we got to the int array
    output = []
    try:
      output = struct.unpack('B' * WIDTH * HEIGHT * 3, line)
    except ValueError:
      self.lastData = line.strip()
      return

    if len(output) != WIDTH*HEIGHT*3:
      self.lastData = line.strip()
      return

    self.visualizeFactory.broadcast(json.dumps(output))
    time.sleep(0.03)

    # Signal for the next frame
    self.lastData = ''
    self.sendMessage("OK")

  def sendMessage(self, message):
    self.transport.write(message + '\n')

class RenderSocketFactory(ReconnectingClientFactory):
  def __init__(self, visualizeFactory):
    self.visualizeFactory = visualizeFactory

  def buildProtocol(self, addr):
    self.resetDelay()
    return RenderSocket(self.visualizeFactory)

  def clientConnectionLost(self, connector, reason):
    ReconnectingClientFactory.clientConnectionLost(self, connector, reason)

  def clientConnectionFailed(self, connector, reason):
    ReconnectingClientFactory.clientConnectionFailed(self, connector,
                                                     reason)
