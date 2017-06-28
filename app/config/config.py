import json

CONFIG_FILE = "config.json"

class Config:
    def __init__(self):
        self.config = {}
        self.readConfig()

    def readConfig(self):
        with open(CONFIG_FILE, 'r+') as f:
            self.config = json.load(f)
