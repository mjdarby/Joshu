import socketserver
from .wakeup import WakeUp
from .setalarm import SetAlarm


class JoshuData():
    def __init__(self):
        self.dataStore = {}

class JoshuHandler(socketserver.BaseRequestHandler):
    def __init__(self, request, client_address, server):
        super(JoshuHandler,self).__init__(request,client_address,server)

    def handle(self):
        self.commands = {"wakeUp": WakeUp(self.server.joshu.dataStore),
                         "setAlarm": SetAlarm(self.server.joshu.dataStore)}

        self.data = self.request.recv(1024).strip().decode("utf-8")
        print("{} wrote: {}".format(self.client_address[0], self.data))

        parameters = self.data.split(" ")
        intent = parameters[0]
        slots = parameters[1:] if len(parameters) > 1 else []

        print(intent)
        print(slots)
        
        if (intent in self.commands.keys()):
            response = self.commands[intent].run(slots)
            self.request.sendall(bytes(response, "utf-8"))
        else:
            self.request.sendall(bytes("Command not found", "utf-8"))

if __name__ == "__main__":
    HOST, PORT = "localhost", 9999
    server = socketserver.TCPServer((HOST, PORT), JoshuHandler)
    server.joshu = JoshuData()
    server.serve_forever()
