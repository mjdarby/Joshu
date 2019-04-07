import boto3
import pyaudio
import time

CHUNK = 16000

def speak(text):
    client = boto3.client('polly')
    response = client.synthesize_speech(
        OutputFormat='pcm',
        Text=text,
        TextType='text',
        VoiceId='Emma',
    )
    # Polly values
    pa = pyaudio.PyAudio()
    output_stream = pa.open(
        rate=CHUNK,
        channels=1,
        format=pyaudio.paInt16,
        output=True,
    )
    body = response['AudioStream']
    data = body.read(CHUNK)
    while len(data) > 0:
        output_stream.write(data)
        data = body.read(CHUNK)
    time.sleep(1) # Bad. Can't get PyAudio to block.
    output_stream.close()
    pa.terminate()
    print(text)
