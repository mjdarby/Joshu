from .command import BaseCommand
from app.cron.cron import Cron, CronJob

class SetAlarm(BaseCommand):
    def __init__(self, dataStore):
        super(SetAlarm, self).__init__("setAlarm")
        self.dataStore = dataStore

    def run(self, connectionInfo, slots):
        cron = Cron()
        cron.addJob("wakeUp", slots[0])
        return "Alarm set for " + slots[0] + " and " + connectionInfo.name
