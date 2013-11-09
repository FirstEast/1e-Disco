from twisted.internet import reactor
from twisted.web.server import Site
from twisted.web.static import File
from autobahn.websocket import listenWS

import pyaudio
import numpy as np
import sys, os

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100

def listen():
  print "starting listener now"
  p = pyaudio.PyAudio()
  stream = p.open(format = FORMAT,
                  channels = CHANNELS,
                  rate = RATE,
                  input = True,
                  output=True,
                  frames_per_buffer = CHUNK)

  while True:
    new_data = stream.read(CHUNK)
    stream.write(new_data, CHUNK)
    rfft = np.fft.rfft([ord(i) for i in new_data])

    bass_freq_range = [20, 140] # Hz
    freq_cutoffs = np.array(bass_freq_range)
    fft_cutoffs = freq_cutoffs * 1024/RATE
    bass = sum([abs(j) for j in rfft[1:fft_cutoffs[1]]])
    if bass < 0:
      bass = 0
    
    midbass_freq_range = [140, 400] # Hz
    freq_cutoffs = np.array(midbass_freq_range)
    fft_cutoffs = freq_cutoffs * 1024/RATE
    midbass = sum([abs(j) for j in rfft[1:fft_cutoffs[1]]])
    if midbass < 0:
      midbass = 0

    mid_freq_range = [400, 2600] # Hz
    freq_cutoffs = np.array(mid_freq_range)
    fft_cutoffs = freq_cutoffs * 1024/RATE
    mid = sum([abs(j) for j in rfft[1:fft_cutoffs[1]]])
    if mid < 0:
      mid = 0

    upmid_freq_range = [2600, 5200] # Hz
    freq_cutoffs = np.array(upmid_freq_range)
    fft_cutoffs = freq_cutoffs * 1024/RATE
    upmid = sum([abs(j) for j in rfft[1:fft_cutoffs[1]]])
    if upmid < 0:
      upmid = 0

    high_freq_range = [5200, 15000] # Hz
    freq_cutoffs = np.array(high_freq_range)
    fft_cutoffs = freq_cutoffs * 1024/RATE
    high = sum([abs(j) for j in rfft[1:fft_cutoffs[1]]])
    if high < 0:
      high = 0

    print str(int(bass)) + " " + str(int(midbass)) + " " + str(int(mid)) + " " + str(int(upmid)) + " " + str(int(high))

if __name__ == '__main__':
  listen()