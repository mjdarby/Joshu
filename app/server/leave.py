import datetime
import time
import random
from .command import BaseCommand
from app.shared.response import Response

class Leave(BaseCommand):
    def __init__(self, dataStore):
        super(Leave, self).__init__("leave")
        self.dataStore = dataStore

    def run(self, connectionInfo, slots):
        if self.dataStore["isUserHome"]:
            self.dataStore["isUserHome"] = False
            return Response(random.choice(["See you soon!", "Have a pleasant day!", "Catch you later."]), "happy")
        else:
            return Response(random.choice(["But you're already out?"]), "neutral")
