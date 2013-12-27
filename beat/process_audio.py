import pyaudio
import sys, os
import math, sys
import numpy
import wave

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
FMT = "%ih" % CHUNK * CHANNELS
RATE = 44100

FFT_SIZE = 2048
RECORD_SECONDS = 0.05
TOTAL_RECORD = 0.5
NUM_SAMPLES = int(RATE / CHUNK * RECORD_SECONDS)
SNIPS = int((TOTAL_RECORD / RECORD_SECONDS) * NUM_SAMPLES)

LAST_FRAMES = [0] * CHUNK * SNIPS

BUCKET_SIZE = 10

P = pyaudio.PyAudio()

clip = lambda val, low, high: min(high, max(low, val))

# Shared beat data object to share between sockets
class BeatData():
  def __init__(self):
    self.leftCentroid = [0]
    self.leftVolume = [0]
    self.leftFrequencies = [0] * BUCKET_SIZE

    self.rightCentroid = [0]
    self.rightVolume = [0]
    self.rightFrequencies = [0] * BUCKET_SIZE

def getAudioStream():
  stream = P.open(format = FORMAT,
                  channels = CHANNELS,
                  rate = RATE,
                  input_device_index = 2,
                  input = True,
                  frames_per_buffer = CHUNK)
  return stream

def processChunk(stream, beatData):
  global LAST_FRAMES
  data = stream.read(CHUNK)
  unpacked = unpack_audio_data(data)[0]
  frames = LAST_FRAMES[CHUNK:] + unpacked

  (centroid, spectrum) = spectral_centroid(frames)

  shortData = frames[-3 * CHUNK:]
  (centroid, shortSpectrum) = spectral_centroid(shortData)
  volume = numpy.sqrt(numpy.mean((shortData-numpy.mean(shortData))**2)) / 2000

  beatData.leftCentroid = centroid
  beatData.leftVolume = volume
  beatData.leftFrequencies = [0] * BUCKET_SIZE

  beatData.rightCentroid = centroid
  beatData.rightVolume = volume
  beatData.rightFrequencies = [0] * BUCKET_SIZE

  LAST_FRAMES = frames

def unpack_audio_data(data):
  """
  Decode the bytearray into one channel of numerical values
  """
  data = wave.struct.unpack(FMT, data)
  channels = [ [] for x in range(CHANNELS) ]

  for index, value in enumerate(data):
      bucket = index % CHANNELS
      channels[bucket].append(value)
  return channels

def spectral_centroid(samples, spec_range=120.0):
  """ starting at seek_point read fft_size samples, and calculate the spectral centroid """
  
  fft = numpy.fft.fft(samples)
  spectrum = numpy.abs(fft[:fft.shape[0] / 2 + 1]) / float(FFT_SIZE) # normalized abs(FFT) between 0 and 1
  length = numpy.float64(spectrum.shape[0])

  # scale the db spectrum from [- spec_range db ... 0 db] > [0..1]
  db_spectrum = ((20*(numpy.log10(spectrum + 1e-30))).clip(-spec_range, 0.0) + spec_range)/spec_range

  energy = spectrum.sum()
  spectral_centroid = 0

  if energy > 1e-20:
    # calculate the spectral centroid

    spectrum_range = numpy.arange(length)

    spectral_centroid = (spectrum * spectrum_range).sum() / (energy * (length - 1)) * RATE * 0.5

    # clip > log10 > scale between 0 and 1
    spectral_centroid = (math.log10(clip(spectral_centroid, 100, 22050)) - math.log10(100)) / (math.log10(22050) - math.log10(100))

  return (spectral_centroid, db_spectrum)