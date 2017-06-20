from threading import RLock
from .client import runClientThread, sendCommand
from app.speechsynth import voice

if __name__ == "__main__":
    # Setup
    lock = RLock()
    clientThread, server = runClientThread(lock)

    # Main loop
    while True:
        data = input(">")
        if data == "quit":
            with lock:
                server.shutdown()
                break

        received = sendCommand(data, lock)
        voice.speak(received)

    # Cleanup
    clientThread.join()
