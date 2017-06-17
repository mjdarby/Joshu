from .command import BaseCommand

class WakeUp(BaseCommand):
    def __init__(self, dataStore):
        super(WakeUp, self).__init__("wake")
        self.dataStore = dataStore

    def run(self, connectionInfo, slots):
        self.dataStore[self.name] = "off"
        return "Wakey-wakey!"
