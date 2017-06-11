import SocketServer
from wakeUp import WakeUp

class JoshuData():
    def __init__(self):
        self.dataStore = {}

class JoshuHandler(socketserver.BaseRequestHandler):
    def __init__(self, request, client_address, server):
        super(JoshuHandler,self).__init__(request,client_address,server)

    def handle(self):
        self.commands = {b"wakeUp": WakeUp(self.server.joshu.dataStore)}

        self.data = self.request.recv(1024).strip()
        print("{} wrote:".format(self.client_address[0]))
        print(self.data)
        if (self.data in self.commands.keys()):
            response = self.commands[self.data].run()
            self.request.sendall(bytes(response, "utf-8"))
        else:
            self.request.sendall(bytes("Command not found", "utf-8"))
        print(self.server.joshu.dataStore["wake"])

if __name__ == "__main__":
    HOST, PORT = "localhost", 9999
    server = socketserver.TCPServer((HOST, PORT), JoshuHandler)
    server.joshu = Joshu()
    server.serve_forever()
