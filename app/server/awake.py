import datetime
import time
from .command import BaseCommand
from app.cron.cron import Cron

class Awake(BaseCommand):
    def __init__(self, dataStore):
        super(Awake, self).__init__("awake")
        self.dataStore = dataStore

    def run(self, connectionInfo, slots):
        # First run check
        if "wake" in self.dataStore.keys():
            self.dataStore["wake"]["awake"] = True
            return "Good morning!"

        return "I know!"
