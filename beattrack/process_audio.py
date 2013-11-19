import pyaudio
import sys, os

import optparse, math, sys
import scikits.audiolab as audiolab
import ImageFilter, ImageChops, Image, ImageDraw, ImageColor
import numpy
  
import contextlib
import wave

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 0.025
NUM_SAMPLES = int(RATE / CHUNK * RECORD_SECONDS)
WAVE_OUTPUT_FILENAME = "output.wav"
LAST_FRAMES = []

BUCKET_SIZE = 10

P = pyaudio.PyAudio()

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
  limit = NUM_SAMPLES * 2
  frames = []
  if len(LAST_FRAMES) != 0:
    frames = LAST_FRAMES[-1*NUM_SAMPLES:]
    limit = NUM_SAMPLES
  for i in range(0, limit):
    data = stream.read(CHUNK)
    frames.append(data)

  wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
  wf.setnchannels(CHANNELS)
  wf.setsampwidth(P.get_sample_size(FORMAT))
  wf.setframerate(RATE)
  wf.writeframes(b''.join(frames))
  wf.close()

  centroid1, frequencies1, volume1 = processWav(WAVE_OUTPUT_FILENAME, 1)
  centroid2, frequencies2, volume2 = processWav(WAVE_OUTPUT_FILENAME, 2)

  beatData.leftCentroid = centroid1[0]
  beatData.leftVolume = volume1[0]
  beatData.leftFrequencies = [0] * BUCKET_SIZE

  beatData.rightCentroid = centroid2[0]
  beatData.rightVolume = volume2[0]
  beatData.rightFrequencies = [0] * BUCKET_SIZE

  LAST_FRAMES = frames


#################
# HERE BE DRAGONS
#################

class AudioProcessor(object):
  def __init__(self, audio_file, fft_size, channel, window_function=numpy.ones):
    self.fft_size = fft_size
    self.window = window_function(self.fft_size)
    self.audio_file = audio_file
    self.frames = audio_file.get_nframes()
    self.samplerate = audio_file.get_samplerate()
    self.channels = audio_file.get_channels()
    self.spectrum_range = None
    self.lower = 100
    self.higher = 22050
    self.lower_log = math.log10(self.lower)
    self.higher_log = math.log10(self.higher)
    self.clip = lambda val, low, high: min(high, max(low, val))
    self.channel = channel
    
  #returns a number of samples from the audio file. 
  def read(self, start, size, resize_if_less=False):
    """ read size samples starting at start, if resize_if_less is True and less than size
    samples are read, resize the array to size and fill with zeros """
 
    # number of zeros to add to start and end of the buffer
    add_to_start = 0
    add_to_end = 0
 
    if start < 0:
      # the first FFT window starts centered around zero
      if size + start <= 0:
        return numpy.zeros(size) if resize_if_less else numpy.array([])
      else:
        self.audio_file.seek(0)
 
        add_to_start = -start # remember: start is negative!
        to_read = size + start
 
        if to_read > self.frames:
          add_to_end = to_read - self.frames
          to_read = self.frames
    else:
      self.audio_file.seek(start)
 
      to_read = size
      if start + to_read >= self.frames:
        to_read = self.frames - start
        add_to_end = size - to_read
 
    try:
      samples = self.audio_file.read_frames(to_read)
    except IOError:
      # this can happen for wave files with broken headers...
      return numpy.zeros(size) if resize_if_less else numpy.zeros(2)
 
    # select which channel to draw
    if self.channels > 1:
      if self.channel==1:
        samples = samples[:,0]
      if self.channel==2:
        samples = samples[:,1]
 
    if resize_if_less and (add_to_start > 0 or add_to_end > 0):
      if add_to_start > 0:
        samples = numpy.concatenate((numpy.zeros(add_to_start), samples), axis=1)
 
      if add_to_end > 0:
        samples = numpy.resize(samples, size)
        samples[size - add_to_end:] = 0
 
    return samples
 
  """
  The spectral centroid is a measure used in digital signal processing to characterise
  a spectrum. It indicates where the "center of mass" of the spectrum is. Perceptually,
  it has a robust connection with the impression of "brightness" of a sound. It is calculated
  as the weighted mean of the frequencies present in the signal, determined using a Fourier
  transform, with their magnitudes as the weights.
  The spectral centroid is widely used in digital audio and music processing as an automatic
  measure of musical timbre. -Wikipedia
  
  Probably extremely useful for visualization.
  """
  def spectral_centroid(self, seek_point, spec_range=120.0):
    """ starting at seek_point read fft_size samples, and calculate the spectral centroid """
    
    samples = self.read(seek_point - self.fft_size/2, self.fft_size, True)
 
    samples *= self.window
    fft = numpy.fft.fft(samples)
    spectrum = numpy.abs(fft[:fft.shape[0] / 2 + 1]) / float(self.fft_size) # normalized abs(FFT) between 0 and 1
    length = numpy.float64(spectrum.shape[0])
 
    # scale the db spectrum from [- spec_range db ... 0 db] > [0..1]
    db_spectrum = ((20*(numpy.log10(spectrum + 1e-30))).clip(-spec_range, 0.0) + spec_range)/spec_range
 
    energy = spectrum.sum()
    spectral_centroid = 0
 
    if energy > 1e-20:
      # calculate the spectral centroid
 
      if self.spectrum_range == None:
        self.spectrum_range = numpy.arange(length)
 
      spectral_centroid = (spectrum * self.spectrum_range).sum() / (energy * (length - 1)) * self.samplerate * 0.5
 
      # clip > log10 > scale between 0 and 1
      spectral_centroid = (math.log10(self.clip(spectral_centroid, self.lower, self.higher)) - self.lower_log) / (self.higher_log - self.lower_log)
 
    return (spectral_centroid, db_spectrum)
 
  #Goes through the samples and finds the min and max amplitudes; used to draw the waveform.
  #This function is probably what I need to use to output amplitudes to a visualizer..
  def peaks(self, start_seek, end_seek):
    """ read all samples between start_seek and end_seek, then find the minimum and maximum peak
    in that range. Returns that pair in the order they were found. So if min was found first,
    it returns (min, max) else the other way around. """
 
    # larger blocksizes are faster but take more mem...
    # Aha, Watson, a clue, a tradeof!
    block_size = 4096
 
    max_index = -1
    max_value = -1
    min_index = -1
    min_value = 1
 
    if end_seek > self.frames:
      end_seek = self.frames
 
    if block_size > end_seek - start_seek:
      block_size = end_seek - start_seek
 
    if block_size <= 1:
      samples = self.read(start_seek, 1)
      return samples[0], samples[0]
    elif block_size == 2:
      samples = self.read(start_seek, True)
      return samples[0], samples[1]
 
    for i in range(start_seek, end_seek, block_size):
      samples = self.read(i, block_size)
 
      local_max_index = numpy.argmax(samples)
      local_max_value = samples[local_max_index]
 
      if local_max_value > max_value:
        max_value = local_max_value
        max_index = local_max_index
 
      local_min_index = numpy.argmin(samples)
      local_min_value = samples[local_min_index]
 
      if local_min_value < min_value:
        min_value = local_min_value
        min_index = local_min_index
 
    return (min_value, max_value) if min_index < max_index else (max_value, min_value)

def processWav(filename, channel):
  """
  filename: path to a wav file
  Channel: 1 for left, 2 for right
  Returns centroids, frequencies, volumes
  """
  #open file
  audio_file = audiolab.sndfile(filename, 'read')

  with contextlib.closing(wave.open(filename, 'r')) as f:
    frames = f.getnframes()
    rate = f.getframerate()
    duration = frames / float(rate)
  duration *= 30 #30 data points for every second of audio yay
  duration = int(duration) #can only return an integer number of frames

  #Not really samples per pixel but I'll let that slide
  samples_per_pixel = audio_file.get_nframes() / float(duration)

  #some rule says this frequency has to be half of the sample rate
  nyquist_freq = (audio_file.get_samplerate() / 2) + 0.0

  #fft_size stays 2048; smaller size == more efficient, fewer frequency samples
  processor = AudioProcessor(audio_file, 2048, channel, numpy.hanning)
  
  centroids = []
  frequencies = []
  volumes = []

  for x in range(duration):
    seek_point = int(x * samples_per_pixel)
    next_seek_point = int((x + 1) * samples_per_pixel)
    (spectral_centroid, db_spectrum) = processor.spectral_centroid(seek_point)
    peaks = processor.peaks(seek_point, next_seek_point)
    
    centroids.append(spectral_centroid)
    frequencies.append(db_spectrum)
    volumes.append(peaks)
  
  #convert volumes[] from peaks to actual volumes
  for i in range(len(volumes)):
    volumes[i] = abs(volumes[i][0]) + abs(volumes[i][1])
  #round frequencies to save resources
  for i in range(len(frequencies)):
    for j in range(len(frequencies[i])):
      frequencies[i][j] = round(frequencies[i][j], 4)
  return centroids, frequencies, volumes