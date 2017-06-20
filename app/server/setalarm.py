import datetime
from .command import BaseCommand
from app.shared.response import Response
from app.cron.cron import Cron

class SetAlarm(BaseCommand):
    def __init__(self, dataStore):
        super(SetAlarm, self).__init__("setAlarm")
        self.dataStore = dataStore

    def run(self, connectionInfo, slots):
        # Reset existing alarm
        if "wake" in self.dataStore.keys():
            self.dataStore["wake"]["awake"] = False
            self.dataStore["wake"]["totalRuns"] = 0

        # Set the wake up event
        cron = Cron()
        cron.addJob("wakeUp", datetime.datetime.fromtimestamp(int(slots[0])))
        responseText = "Alarm set for " + slots[0] + " and " + connectionInfo.name
        response = Response(responseText, "neutral")
        return response
