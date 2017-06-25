import datetime
import time
import random
from .command import BaseCommand
from app.shared.response import Response
from app.cron.cron import Cron

class Chat(BaseCommand):
    def __init__(self, dataStore):
        super(Chat, self).__init__("chat")
        self.dataStore = dataStore

    def run(self, connectionInfo, slots):
        # TODO Try and work out what the user wants, and then do it
        return Response(random.choice(["Really?", "That's interesting", "lol"]), "neutral")
