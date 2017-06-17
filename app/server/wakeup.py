import datetime
import time
import random
from .command import BaseCommand
from app.cron.cron import Cron

class WakeUp(BaseCommand):
    def __init__(self, dataStore):
        super(WakeUp, self).__init__("wake")
        self.dataStore = dataStore

    def getWakeUpString(self):
        if (self.getData("totalRuns") == 0):
            return random.choice(["Time to wake up!", "Rise and shine!"])
        else:
            return random.choice(["Hey, get up already!", "Don't make me repeat myself!"])

    def run(self, connectionInfo, slots):
        # First run check
        if self.name not in self.dataStore.keys():
            self.dataStore[self.name] = {"awake": False, "totalRuns": 0}

        if not self.dataStore[self.name]["awake"]:
            cron = Cron()
            cron.addJob("wakeUp", datetime.datetime.fromtimestamp(int(time.time())+10))
            wakeUpString = self.getWakeUpString()
            self.dataStore[self.name]["totalRuns"] += 1
            return wakeUpString
        else:
            return ""
