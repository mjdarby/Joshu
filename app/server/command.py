class BaseCommand:
    def __init__(self, name):
        self.name = name
    
    def run(self, connectionInfo, slots):
        pass
