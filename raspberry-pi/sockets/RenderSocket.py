from twisted.internet.protocol import Protocol, ReconnectingClientFactory

import time
import struct
import RPi.GPIO as GPIO

dev = "/dev/spidev0.0"
spidev = file(dev, "wb")

class RenderSocket(Protocol):
  def __init__(self, length):
    self.length = length

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
      output = struct.unpack('B'*self.length*3, line)
    except struct.error:
      self.sendMessage("OK")
      return

    spidev.write(bytearray(output))
    spidev.flush()

    # Signal for the next frame
    self.sendMessage("OK")

  def sendMessage(self, message):
    self.transport.write(message + '\n')

class RenderSocketFactory(ReconnectingClientFactory):
  def __init__(self, length):
    self.length = length

  def buildProtocol(self, addr):
    self.resetDelay()
    return RenderSocket(self.length)

  def clientConnectionLost(self, connector, reason):
    ReconnectingClientFactory.clientConnectionLost(self, connector, reason)

  def clientConnectionFailed(self, connector, reason):
    ReconnectingClientFactory.clientConnectionFailed(self, connector,
                                                     reason)
