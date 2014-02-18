import pyaudio
import sys, os
import math, sys
import numpy
import wave

from pylab import *

CHUNK = 2048
FORMAT = pyaudio.paInt16
CHANNELS = 1
FMT = "%ih" % CHUNK * CHANNELS
RATE = 44100

LAST_FRAMES = [0] * CHUNK * 2

BUCKET_SIZE = 48

FR = 1 / float(CHUNK*2.0/RATE)
LOW = 64
HIGH = 16384
SCALE = (HIGH/LOW)**(1.0/BUCKET_SIZE)

P = pyaudio.PyAudio()

clip = lambda val, low, high: min(high, max(low, val))

def getAudioStream(input):
  stream = P.open(format = FORMAT,
                  channels = CHANNELS,
                  rate = RATE,
                  input_device_index = int(input),
                  input = True,
                  frames_per_buffer = CHUNK)
  return stream

class WaveStream():
  def __init__(self, filename):
    self.wf = wave.open(filename, 'rb')
  def read(self, chunkSize):
    return self.wf.readframes(chunkSize)

class AudioProcessor():
  def __init__(self, stream):
    self.stream = stream
    self.lastFrames = [0] * CHUNK * 2
    self.centroid = 0
    self.volume = 0
    self.frequencies = [0] * BUCKET_SIZE

  def getBeatData(self):
    return {
      'centroid': self.centroid,
      'volume': self.volume,
      'frequencies': self.frequencies
    }

  def processChunk(self):
    data = self.stream.read(CHUNK)
    unpacked = self.unpack_audio_data(data)[0]
    frames = self.lastFrames[CHUNK:] + unpacked

    volume = numpy.sqrt(numpy.mean((frames-numpy.mean(frames))**2)) / (2**13)

    if volume == 0:
      centroid = 0
      freqs = [0] * BUCKET_SIZE
    else:
      (centroid, spectrum) = self.spectral_centroid(frames)

      freqs = []
      current = LOW
      while current < HIGH:
        total = numpy.sum(spectrum[int(current/FR):int(current*SCALE/FR)])
        freqs.append((total / (int(current*SCALE/FR) - int(current/FR))))
        current = int(current * SCALE)
      freqs = freqs[:-1]

    self.centroid= centroid
    self.volume = volume
    self.frequencies = freqs

    self.lastFrames = frames

  def unpack_audio_data(self, data):
    """
    Decode the bytearray into one channel of numerical values
    """
    data = wave.struct.unpack(FMT, data)
    channels = [ [] for x in range(CHANNELS) ]

    for index, value in enumerate(data):
        bucket = index % CHANNELS
        channels[bucket].append(value)
    return channels

  def spectral_centroid(self, samples, spec_range=200.0):
    """ starting at seek_point read fft_size samples, and calculate the spectral centroid """

    hanning = numpy.hanning(len(samples))

    fft = numpy.fft.fft(hanning * samples)
    stuff = numpy.abs(fft[:fft.shape[0] / 2 + 1])
    spectrum = stuff / (numpy.sqrt(fft.size))
    length = numpy.float64(spectrum.shape[0])

    # scale the db spectrum from [- spec_range db ... 0 db] > [0..1]
    db_spectrum = 20*numpy.log10(spectrum + 1e-30)
    db_spectrum = db_spectrum - numpy.max(db_spectrum)
    db_spectrum = (db_spectrum.clip(-spec_range, 0.0) + spec_range)/spec_range

    energy = spectrum.sum()
    spectral_centroid = 0

    if energy > 1e-20:
      # calculate the spectral centroid

      spectrum_range = numpy.arange(length)

      spectral_centroid = (spectrum * spectrum_range).sum() / (energy * (length - 1)) * RATE * 0.5

      # clip > log10 > scale between 0 and 1
      spectral_centroid = (math.log10(clip(spectral_centroid, LOW, HIGH)) - math.log10(LOW)) / (math.log10(HIGH) - math.log10(LOW))

    return (spectral_centroid, db_spectrum)
