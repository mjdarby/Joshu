import pyttsx
import command

class WakeUp(command.BaseCommand):
    def __init__(self, dataStore):
        self.dataStore = dataStore

    def run(self):
        print("I'm running!")
        self.dataStore["wake"] = "off"
        engine = pyttsx.init()
        engine.say('Wake up')
        engine.runAndWait()
        return "Wakey-wakey!"
