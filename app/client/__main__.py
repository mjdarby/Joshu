import sys
from threading import RLock
from .client import runClientThread, sendCommand
from app.shared.response import Response
from app.speechsynth import voice

if __name__ == "__main__":
    host = sys.argv[1]

    def callback(data):
        response = Response.decodeJson(data)
        voice.speak(response.text)

    # Setup
    lock = RLock()
    clientThread, server = runClientThread(lock, callback)

    # Main loop
    while True:
        data = input(">")
        if data == "quit":
            with lock:
                server.shutdown()
                break

        received = sendCommand(host, data, lock)
        response = Response.decodeJson(received)
        voice.speak(response.text)

    # Cleanup
    clientThread.join()
