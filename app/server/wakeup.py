import datetime
import time
import random
from .command import BaseCommand
from app.shared.response import Response
from app.cron.cron import Cron

class WakeUp(BaseCommand):
    def __init__(self, dataStore):
        super(WakeUp, self).__init__("wake")
        self.dataStore = dataStore

    def getWakeUpResponse(self):
        responseText = ""
        responseMood = ""
        if (self.getData("totalRuns") == 0):
            return Response(random.choice(["Time to wake up!", "Rise and shine!"]), "happy")
        else:
            return Response(random.choice(["Hey, get up already!", "Don't make me repeat myself!"]), "annoyed")

    def run(self, connectionInfo, slots):
        # First run check
        if self.name not in self.dataStore.keys():
            self.dataStore[self.name] = {"awake": False, "totalRuns": 0}

        if not self.dataStore[self.name]["awake"]:
            cron = Cron()
            cron.addJob("wakeUp", datetime.datetime.fromtimestamp(int(time.time())+10))
            wakeUpResponse = self.getWakeUpResponse()
            self.dataStore[self.name]["totalRuns"] += 1
            return wakeUpResponse
        else:
            return ""
