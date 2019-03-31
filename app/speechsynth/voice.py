# import win32com.client

voice = 'Microsoft Sam'
volume = 100
rate = -1

def speak(text):
#    speak = win32com.client.Dispatch('Sapi.SpVoice')
#    speak.Voice = speak.GetVoices('Name='+voice).Item(0)
#    speak.Rate = rate
#    speak.Volume = volume
#    speak.Speak(text)
    print(text)
