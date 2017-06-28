import datetime
import time
import random
from .command import BaseCommand
from app.shared.response import Response

class Home(BaseCommand):
    def __init__(self, dataStore):
        super(Home, self).__init__("home")
        self.dataStore = dataStore

    def run(self, connectionInfo, slots):
        if self.dataStore["isUserHome"]:
            return Response(random.choice(["But you're already home?"]), "neutral")
        else:
            self.dataStore["isUserHome"] = True
            return Response(random.choice(["Welcome home!", "How was it out?", "Welcome back."]), "happy")
