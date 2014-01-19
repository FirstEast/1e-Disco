from twisted.internet.protocol import Protocol, ReconnectingClientFactory

import time
import struct

try:
  import RPi.GPIO as GPIO
  raspi = True
  dev = "/dev/spidev0.0"
  spidev = file(dev, "wb")
except ImportError:
  raspi = False

LENGTH = 261

class RenderSocket(Protocol):
  def connectionMade(self):
    print "connected successfully to central server"

    time.sleep(1)

    # Signal for the next frame
    self.sendMessage("OK")

  def dataReceived(self, line):
    # Parse what we got to the int array
    line = line.strip()
    output = []
    try:
      output = struct.unpack('B'*LENGTH*3, line)
    except struct.error:
      self.sendMessage("OK")
      return

    # If we're running on a raspi, render the stuff we got,
    # otherwise send it to the web visualizer as json
    if raspi:
      spidev.write(bytearray(output))
      spidev.flush()

    # Signal for the next frame
    self.sendMessage("OK")

  def sendMessage(self, message):
    self.transport.write(message + '\n')

class RenderSocketFactory(ReconnectingClientFactory):
  def buildProtocol(self, addr):
    self.resetDelay()
    return RenderSocket()

  def clientConnectionLost(self, connector, reason):
    ReconnectingClientFactory.clientConnectionLost(self, connector, reason)

  def clientConnectionFailed(self, connector, reason):
    ReconnectingClientFactory.clientConnectionFailed(self, connector,
                                                     reason)
