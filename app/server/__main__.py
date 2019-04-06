import datetime
import socketserver
import threading
import time
import socket
from .wakeup import WakeUp
from .setalarm import SetAlarm
from .awake import Awake
from .chat import Chat
from .weather import Weather
from .home import Home
from .leave import Leave
from .encouragement import Encouragement
from .command import BaseCommand
from app.shared.response import Response
from app.cron.cron import Cron

class ConnectionInfo():
    def __init__(self, ip, name):
        self.ip = ip
        self.name = name

    def __repr__(self):
        return self.ip + ": " + self.name

class Connect(BaseCommand):
    def __init__(self, dataStore):
        super(Connect, self).__init__("connect")
        self.dataStore = dataStore

    def run(self, connectionInfo, slots):
        responseText = ""
        if connectionInfo.ip in self.dataStore["connectedClients"].keys():
            responseText = "Already connected"
        else:
            connectionInfo.name = slots[0]
            self.dataStore["connectedClients"][connectionInfo.ip] = connectionInfo
            responseText = "Connected as " + connectionInfo.name
        response = Response(responseText, "happy")
        return response

class Disconnect(BaseCommand):
    def __init__(self, dataStore):
        super(Disconnect, self).__init__("disconnect")
        self.dataStore = dataStore

    def run(self, connectionInfo, slots):
        responseText = ""
        if connectionInfo.ip in self.dataStore["connectedClients"].keys():
            del self.dataStore["connectedClients"][connectionInfo.ip]
            responseText = "Disconnected"
        else:
            responseText = "Not connected"
        response = Response(responseText, "neutral")
        return response

class CommandList():
    def __init__(self, dataStore):
        self.commands = {"connect": Connect(dataStore),
                         "disconnect": Disconnect(dataStore),
                         "weather": Weather(dataStore),
                         "wakeUp": WakeUp(dataStore),
                         "setalarm": SetAlarm(dataStore),
                         "awake": Awake(dataStore),
                         "chat": Chat(dataStore),
                         "home": Home(dataStore),
                         "leave": Leave(dataStore),
                         "encouragement": Encouragement(dataStore)}

class JoshuData():
    def __init__(self):
        self.dataStore = {}

    def initialise(self):
        self.dataStore["isUserHome"] = True
        self.dataStore["isUserAtWork"] = False
        self.dataStore["connectedClients"] = {}

class JoshuHandler(socketserver.BaseRequestHandler):
    def __init__(self, request, client_address, server):
        super(JoshuHandler,self).__init__(request,client_address,server)

    def handle(self):
        with lock:
            self._handle()

    def _handle(self):
        self.commands = CommandList(self.server.joshu.dataStore).commands
        self.data = self.request.recv(102400).strip()
        print(self.data)
        dataType = self.data[0]
        self.data = self.data[1:]

        if dataType == 0: # Text
            self.data = self.data.decode('utf-8')
            print("{} wrote: {}".format(self.client_address[0], self.data))
            print(len(self.data))
        else: # Voice
            print("Voice command received")
            print(len(self.data))
            f = open("output.wav", 'wb')
            f.write(self.data)
            f.close()
            self.data = 'connect home' # TODO Fix it

        parameters = self.data.split(" ")
        intent = parameters[0]
        slots = parameters[1:] if len(parameters) > 1 else []

        print(intent)
        print(slots)
        print(self.server.joshu.dataStore["connectedClients"])

        # 'Auth'
        connectionInfo = None
        if self.client_address[0] in self.server.joshu.dataStore["connectedClients"].keys():
            connectionInfo = self.server.joshu.dataStore["connectedClients"][self.client_address[0]]
            print("Message from: {} at IP {}".format(connectionInfo.name, connectionInfo.ip))
        elif intent == "connect":
            connectionInfo = ConnectionInfo(self.client_address[0], "")
        else:
            response = Response("Not authorised", "neutral")
            self.request.sendall(bytes(response.getJson(), "utf-8"))
            return

        # Run command
        if (intent in self.commands.keys()):
            response = self.commands[intent].run(connectionInfo, slots)
            self.request.sendall(bytes(response.getJson(), "utf-8"))
        else:
            response = Response("Command not found", "neutral")
            self.request.sendall(bytes(response.getJson(), "utf-8"))

lock = threading.RLock()
serverRunning = True
sharedData = JoshuData()
sharedData.initialise()

def runServer(cronThread):
    global serverRunning
    try:
        HOST, PORT = "", 9999
        server = socketserver.TCPServer((HOST, PORT), JoshuHandler)
        server.joshu = sharedData
        server.serve_forever()
        with lock:
            serverRunning = False
        cronThread.join()
    except KeyboardInterrupt:
        serverRunning = False
        raise

def sendToClient(clientIp, response):
    HOST, PORT = clientIp, 4500

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock.connect((HOST,PORT))
        sock.sendall(bytes(response.getJson(), "utf-8"))
        received = str(sock.recv(1024), "utf-8") # TODO Timeout
    finally:
        sock.close()

def runCron():
    cron = Cron()
    commandList = CommandList(sharedData.dataStore).commands

    # Clear cron file
    cron.writeJobs([])

    # Add initial cron items
    cron.addJob("encouragement", datetime.datetime.fromtimestamp(int(time.time())+5))

    # TODO Add user-configured cron actions

    # Run cron loop
    while serverRunning:
        with lock:
            # Tidy dead connections
            HOST, PORT = "localhost", 4500

            # Run cron
            jobsToRun = cron.run()
            for job in jobsToRun:
                print(job)
                # Run job
                if job.string in commandList.keys():
                    response = commandList[job.string].run(None, job.slots) # Cron jobs should be connection agnostic
                    if response:
                        # Send output to either all clients, or target client
                        for clientIp in sharedData.dataStore["connectedClients"].keys():
                            connectionDetails = sharedData.dataStore["connectedClients"][clientIp]
                            if job.targetName == None or connectionDetails.name == job.targetName:
                                sendToClient(clientIp, response)
                else:
                    print("Command not found IN CRONJOB! " + job.string)

            time.sleep(1)

if __name__ == "__main__":
    cronThread = threading.Thread(None, runCron)
    cronThread.start()
    runServer(cronThread)
