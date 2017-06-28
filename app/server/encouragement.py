import datetime
import time
import random
from .command import BaseCommand
from app.shared.response import Response
from app.cron.cron import Cron
from app.config.config import Config

class Encouragement(BaseCommand):
    def __init__(self, dataStore):
        super(Encouragement, self).__init__("encouragement")
        self.dataStore = dataStore
        self.dataStore["encouragement"] = {}
        self.dataStore["encouragement"]["lastCalled"] = None

    def run(self, connectionInfo, slots):
        response = None

        # Determine if the user should be at work
        config = Config()
        workdays = config.config["work"]["workdays"]
        worktimes = (config.config["work"]["workStart"], config.config["work"]["workEnd"])
        worktimes = (time.strftime("%H:%M", worktimes[0]), time.strftime("%H:%M", worktimes[1]))
        currentTime = datetime.datetime.today().time()
        userAtWork = datetime.datetime.today().weekday() in workdays and (worktimes[0] < currentTime and currentTime < worktimes[1])

        # If they're not in and they're meant to be at work, send encouragement
        if not self.dataStore["isUserHome"] and userAtWork:
            # Update last called time
            self.dataStore["encouragement"]["lastCalled"] = datetime.datetime.now()

            # TODO Send encouragement via FCM to messenger
            # For now, return response
            response = Response(random.choice(["Hope work is going well!"]), "happy")
        self.enqueue(60)
        return response

    def enqueue(self, seconds):
        cron = Cron()
        cron.addJob("encouragement", datetime.datetime.fromtimestamp(int(time.time())+seconds))

