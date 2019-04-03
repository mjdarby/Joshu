import speech_recognition as sr

import boto3
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
    return frames
    wf = wave.open("input.wav", 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(pa.get_sample_size(pyaudio.paInt16))
    wf.setframerate(porcupine.sample_rate)
    wf.writeframes(bytes(frames))

def getAudio(porcupine, pa, audio_stream):
    frames = recordUntilSilent(porcupine, pa, audio_stream)
    client = boto3.client('lex-runtime')
    ret = client.post_content(
        botName='Joshu',
        botAlias='Test',
        userId='abc123',
        contentType='audio/l16; rate=16000; channels=1',
        accept='text/plain; charset=utf-8',
        inputStream=bytes(frames))

    # TODO: Actual conversation until error or intent w/ slots returned

    # Hacky debug stuff
    if 'intentName' in ret and ret['dialogState'] == 'ReadyForFulfillment':
        print(ret['intentName'])
        slots = {}
        if 'slots' in ret:
            slots = ret['slots']
        return True, ret['intentName'].lower(), slots
    elif ret['dialogState'] == 'ElicitSlot':
        # TODO: Automatically retrigger getAudio after response has played
        return False, ret['message'], {}
    else:
        # End of conversation
        return False, ret['message'], {}

    return False, "Here be problems!"
