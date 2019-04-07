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

def runHotwordThread(callback, porcupine, pa, audio_stream, isRunning):
    hotwordThread = Thread(None, target=run, args=(callback, porcupine, pa, audio_stream, isRunning))
    hotwordThread.start()
    return hotwordThread

def run(callback, porcupine, pa, audio_stream, isRunning):
    try:
        while True:
            is_running = isRunning()
            if not is_running:
                raise KeyboardInterrupt("Time to go.")

            pcm = audio_stream.read(porcupine.frame_length, exception_on_overflow=False)
            pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

            result = porcupine.process(pcm)
            if result:
                print('[%s] detected keyword, start recording' % str(datetime.now()))
                callback()

    except KeyboardInterrupt:
        print('stopping ...')
    finally:
        if porcupine is not None:
            porcupine.delete()

        if audio_stream is not None:
            audio_stream.close()

        if pa is not None:
            pa.terminate()
