import boto3
import pyaudio

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
        rate=16000,
        channels=1,
        format=pyaudio.paInt16,
        output=True,
    )
    body = response['AudioStream']
    data = body.read(16000)
    while len(data) > 0:
        output_stream.write(data)
        print(data)
        data = body.read(16000)
    print(text)
