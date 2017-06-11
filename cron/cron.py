import socket
import sys
import time
import datetime

class CronJob():
    def __init__(self, time, string):
        self.executionTime = time
        self.string = string

class Cron():
    def __init__(self):
        self.jobs = []
        self.currentTime = datetime.datetime.now()

    def sendData(self, string):
        HOST, PORT = "localhost", 9999
        data = string

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            sock.connect((HOST,PORT))
            sock.sendall(bytes(data, "utf-8"))
            received = str(sock.recv(1024), "utf-8")
        finally:
            sock.close()

        print("Sent: {}".format(data))
        print("Received: {}".format(received))

    def run(self):
        timeAtStartOfRun = datetime.datetime.now()
        for job in self.jobs:
            print(job.executionTime)
            print(self.currentTime)
            # ie. if this event should happen now...
            if self.currentTime < job.executionTime and job.executionTime < timeAtStartOfRun:
                self.sendData(job.string)
        self.currentTime = timeAtStartOfRun

if __name__ == "__main__":
    cron = Cron()
    cron.jobs = [CronJob(datetime.datetime.now() + datetime.timedelta(0, 10), "wakeUp")]
    while True:
        time.sleep(1)
        cron.run()
