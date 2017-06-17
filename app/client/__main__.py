import socketserver
import socket
import sys
import threading
from app.speechsynth import voice

lock = threading.RLock()
clientRunning = True

class ClientHandler(socketserver.BaseRequestHandler):
    def handle(self):
        with lock:
            self._handle()

    def _handle(self):
        if not clientRunning:
            self.shutdown()
        data = self.request.recv(1024).strip().decode("utf-8")
        self.request.sendall(bytes("ACK", "utf-8"))
        voice.speak(data)


def runClient(server):
    server.serve_forever()

if __name__ == "__main__":
    HOST, PORT = "localhost", 4500
    server = socketserver.TCPServer((HOST, PORT), ClientHandler)
    clientThread = threading.Thread(None, server.serve_forever)
    clientThread.start()

    HOST, PORT = "localhost", 9999
    data = ""

    while True:
        data = input(">")
        if data == "quit":
            with lock:
                server.shutdown()
                clientRunning = False
                break

        with lock:
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

    clientThread.join()

