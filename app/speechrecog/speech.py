import speech_recognition as sr
def getAudio():
    r = sr.Recognizer()
    m = sr.Microphone()
    
    with m as source: audio = r.listen(source)
    print("Got it! Now to recognize it...")
    try:
        # recognize speech using Google Speech Recognition
        value = r.recognize_google(audio)
        return True, value
    except sr.UnknownValueError:
        return False,  "Oops! Didn't catch that"
    except sr.RequestError as e:
        return False,  "I'm not feeling well. Try me again later."

