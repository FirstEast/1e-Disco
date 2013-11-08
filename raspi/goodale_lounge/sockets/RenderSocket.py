from twisted.internet.protocol import Protocol, ReconnectingClientFactory

import cPickle as pickle
import json

try:
  import RPi.GPIO as GPIO
  raspi = True
  dev = "/dev/spidev0.0"
  spidev = file(dev, "wb")
except ImportError:
  raspi = False

class RenderSocket(Protocol):
  def connectionMade(self):
    print "connected successfully to central server"

    # Signal for the next frame
    self.sendMessage("OK")

  def dataReceived(self, line):
    # Parse what we got to the int array
    output = pickle.loads(line)

    # If we're running on a raspi, render the stuff we got,
    # otherwise send it to the web visualizer as json
    if raspi:
      spidev.write(output)
      spidev.flush()
    else:
      self.visualizeFactory.broadcast(json.dumps(line))

    # Signal for the next frame
    self.sendMessage("OK")

  def sendMessage(self, message):
    self.transport.write(message + '\n')

class RenderSocketFactory(ReconnectingClientFactory):
  def __init__(self, visualizeFactory):
    self.visualizeFactory = visualizeFactory

  def buildProtocol(self, addr):
    self.resetDelay()
    return RenderSocket()

  def clientConnectionLost(self, connector, reason):
    ReconnectingClientFactory.clientConnectionLost(self, connector, reason)

  def clientConnectionFailed(self, connector, reason):
    ReconnectingClientFactory.clientConnectionFailed(self, connector,
                                                     reason)