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

    def writeJobs(self, jobs):
        with open('crontab', 'w') as f:
            for job in jobs:
                f.write(str(int(job.executionTime.timestamp())) + " " + job.string + '\n')

    def addJob(self, intent, time):
        jobs = self.getJobs()
        jobs.append(CronJob(time, intent))
        self.writeJobs(jobs)

    def deleteJob(self, intent):
        self.jobs = self.getJobs()
        newJobs = []
        for job in self.jobs:
            if job.string != intent:
                newJobs.append(job)
        self.writeJobs(self, newJobs)
        self.jobs = newJobs

    def getJobs(self):
        jobs = []
        with open('crontab', 'r+') as f:
            for line in f:
                line = line[0:-1] # Strip newline
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
                print("Running job")
                jobsToRun.append(job)
        self.currentTime = timeAtStartOfRun
        return jobsToRun

