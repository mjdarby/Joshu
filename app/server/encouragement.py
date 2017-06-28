import datetime
import time
import random
from .command import BaseCommand
from app.shared.response import Response
from app.cron.cron import Cron

class Encouragement(BaseCommand):
    def __init__(self, dataStore):
        super(Encouragement, self).__init__("encouragement")
        self.dataStore = dataStore
        self.dataStore["encouragement"] = {}
        self.dataStore["encouragement"]["lastCalled"] = None

    def run(self, connectionInfo, slots):
        if not self.dataStore["isUserHome"]: # TODO and self.dataStore["isUserAtWork"]:
            # Update last called time
            self.dataStore["encouragement"]["lastCalled"] = datetime.datetime.now()

            # Re-enqueue
            self.enqueue(60)

            # TODO Send encouragement via FCM to messenger
            # For now, return response
            return Response(random.choice(["Hope work is going well!"]), "happy")
        else:
            # Re-enqueue for a minute later
            self.enqueue(60)
            return None

    def enqueue(self, seconds):
        cron = Cron()
        cron.addJob("encouragement", datetime.datetime.fromtimestamp(int(time.time())+seconds))

