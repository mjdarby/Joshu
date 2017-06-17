import time

from .cron import Cron

if __name__ == "__main__":
    cron = Cron()
    while True:
        time.sleep(1)
        cron.run()
