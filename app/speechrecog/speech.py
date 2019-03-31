import speech_recognition as sr

import argparse
import os
import platform
import struct
import sys
from datetime import datetime
from threading import Thread
from array import array
import wave
import audioop

import numpy as np
import pyaudio
import soundfile

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../Porcupine/binding/python'))
from porcupine import Porcupine

def recordUntilSilent(porcupine, pa, audio_stream):
    record = True
    frames = array('h')
    silent_frames = 0
    while record:
        pcm = audio_stream.read(porcupine.frame_length)
        avg = audioop.rms(pcm, 2)
        print(avg)
        frames.extend(array('h', pcm))
        if avg < 200:
            silent_frames += 1
        else:
            silent_frames = 0
        if silent_frames > 30:
            record = False
    wf = wave.open("input.wav", 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(pa.get_sample_size(pyaudio.paInt16))
    wf.setframerate(porcupine.sample_rate)
    wf.writeframes(bytes(frames))

def getAudio(porcupine, pa, audio_stream):
    recordUntilSilent(porcupine, pa, audio_stream)
    # Do some Lex stuff
    return False, "Be patient, we haven't done this part yet."
