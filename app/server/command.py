class BaseCommand:
    def __init__(self, name):
        self.name = name

    def getData(self, string):
        return self.dataStore[self.name][string]
    
    def run(self, connectionInfo, slots):
        pass
