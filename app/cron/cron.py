import socket
import sys
import datetime

class CronJob():
    def __init__(self, time, string):
        self.executionTime = time
        self.string = string
        self.targetName = None

class Cron():
    def __init__(self):
        self.jobs = []
        self.currentTime = datetime.datetime.now()

    def sendData(self, string):
        HOST, PORT = "localhost", 4500
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

    def writeJobs(self, jobs):
        with open('crontab', 'w') as f:
            for job in jobs:
                f.write(job.executionTime + " " + job.string)

    def addJob(self, intent, time):
        self.jobs.append(CronJob(time, intent))
        self.writeJobs(self.jobs)

    def deleteJob(self, intent):
        jobs = []
        for job in self.jobs:
            if job.string != intent:
                jobs.append(job)
        self.jobs = jobs

    def getJobs(self):
        jobs = []
        with open('crontab', 'r+') as f:
            for line in f:
                print(line)
                parameters = line.split(" ")
                jobs.append(CronJob(datetime.datetime.fromtimestamp(int(parameters[0])), parameters[1]))
        return jobs
                

    def run(self):
        timeAtStartOfRun = datetime.datetime.now()
        jobsToRun = []
        # Get list of jobs
        self.jobs = self.getJobs()
        for job in self.jobs:
            print(job.executionTime)
            print(self.currentTime)
            # ie. if this event should happen now...
            if self.currentTime < job.executionTime and job.executionTime < timeAtStartOfRun:
                jobsToRun.append(job)
        self.currentTime = timeAtStartOfRun
        return jobsToRun

