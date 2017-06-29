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
        workTimes = (config.config["work"]["workStart"], config.config["work"]["workEnd"])
        workTimes = (time.strptime(workTimes[0], "%H:%M"), time.strptime(workTimes[1], "%H:%M"))
        workTimes = (datetime.datetime.today().replace(hour=workTimes[0].tm_hour, minute=workTimes[0].tm_min), datetime.datetime.today().replace(hour=workTimes[1].tm_hour, minute=workTimes[1].tm_min))
        halfwayThroughDay = workTimes[0] + datetime.timedelta(seconds=(workTimes[1] - workTimes[0]).total_seconds()/2)
        currentTime = datetime.datetime.now()

        # If they're not in and they're meant to be at work, send encouragement halfway through the day
        userAtWork = datetime.datetime.today().weekday() in workdays and (workTimes[0] < currentTime and currentTime < workTimes[1])
        shouldSendEncouragement = not self.dataStore["isUserHome"] and userAtWork

        # Have we already done this today?
        shouldSendEncouragement = shouldSendEncouragement and self.dataStore["encouragement"]["lastCalled"] != datetime.datetime.today().date()

        # Is it the right time of day?
        shouldSendEncouragement = shouldSendEncouragement and (currentTime > halfwayThroughDay)

        if shouldSendEncouragement:
            # Update last called time
            self.dataStore["encouragement"]["lastCalled"] = datetime.datetime.today().date()

            # TODO Send encouragement via FCM to messenger
            # For now, return response
            response = Response(random.choice(["Hope work is going well!"]), "happy")
        self.enqueue(60)
        return response

    def enqueue(self, seconds):
        cron = Cron()
        cron.addJob("encouragement", datetime.datetime.fromtimestamp(int(time.time())+seconds))

