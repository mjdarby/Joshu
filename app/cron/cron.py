import socket
import sys
import datetime
import json

class CronJob():
    def __init__(self, time, string, targetName, slots):
        self.executionTime = time
        self.string = string
        self.targetName = targetName
        self.slots = slots

    def returnAsJson(self):
        jsonDict = {"executionTime": int(self.executionTime.timestamp()),
                    "string": self.string,
                    "slots": self.slots}
        if self.targetName:
            jsonDict["targetName"] = self.targetName
        return json.dumps(jsonDict)

    def getFromJson(jsonString):
        jsonDict = json.loads(jsonString)
        if "targetName" in jsonDict.keys():
            return CronJob(datetime.datetime.fromtimestamp(int(jsonDict["executionTime"])), jsonDict["string"], jsonDict["targetName"], jsonDict["slots"])
        else:
            return CronJob(datetime.datetime.fromtimestamp(int(jsonDict["executionTime"])), jsonDict["string"], None, jsonDict["slots"])

class Cron():
    def __init__(self):
        self.jobs = []
        self.currentTime = datetime.datetime.now()

    def writeJobs(self, jobs):
        with open('crontab', 'w') as f:
            for job in jobs:
                f.write(job.returnAsJson() + '\n')

    def addJob(self, intent, time, targetName=None, slots=[]):
        jobs = self.getJobs()
        jobs.append(CronJob(time, intent, targetName, slots))
        self.writeJobs(jobs)

    def deleteJob(self, intent):
        self.jobs = self.getJobs()
        newJobs = []
        for job in self.jobs:
            if job.string != intent:
                newJobs.append(job)
        self.writeJobs(newJobs)
        self.jobs = newJobs

    def getJobs(self):
        jobs = []
        with open('crontab', 'r+') as f:
            for line in f:
                line = line[0:-1] # Strip newline
                print(line)
                job = CronJob.getFromJson(line)
                jobs.append(job)
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
            # Delete it from the file
            if job.executionTime < timeAtStartOfRun:
                self.deleteJob(job.string)
            # Run it - allows for self re-enque
            if self.currentTime < job.executionTime and job.executionTime < timeAtStartOfRun:
                print("Running job")
                jobsToRun.append(job)
                
        self.currentTime = timeAtStartOfRun
        return jobsToRun

