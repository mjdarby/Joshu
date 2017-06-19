import socketserver
import socket
import threading
from app.speechsynth import voice

class ClientHandler(socketserver.BaseRequestHandler):
    def handle(self):
        with self.server.lock:
            self._handle()

    def _handle(self):
        data = self.request.recv(1024).strip().decode("utf-8")
        self.request.sendall(bytes("ACK", "utf-8"))
        voice.speak(data)

def runClientThread(clientLock):
    HOST, PORT = "localhost", 4500
    server = socketserver.TCPServer((HOST, PORT), ClientHandler)
    server.lock = clientLock
    clientThread = threading.Thread(None, server.serve_forever)
    clientThread.start()
    return clientThread, server

def sendCommand(data, clientLock):
    HOST, PORT = "localhost", 9999
    with clientLock:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            sock.connect((HOST,PORT))
            sock.sendall(bytes(data, "utf-8"))
            received = str(sock.recv(1024), "utf-8")
        finally:
            sock.close()

        print("Sent: {}".format(data))
        print("Received: {}".format(received))
        voice.speak(received)    

