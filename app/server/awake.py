import datetime
import time
import random
from .command import BaseCommand
from app.shared.response import Response
from app.cron.cron import Cron

class Awake(BaseCommand):
    def __init__(self, dataStore):
        super(Awake, self).__init__("awake")
        self.dataStore = dataStore

    def run(self, connectionInfo, slots):
        # First run check
        if "wake" in self.dataStore.keys():
            self.dataStore["wake"]["awake"] = True
            return Response(random.choice(["Ta-da!", ""]), "happy")
        return Response(random.choice(["There's no alarm to turn off."]), "neutral")
