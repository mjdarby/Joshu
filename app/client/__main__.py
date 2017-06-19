from threading import RLock
from .client import runClientThread, sendCommand

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

        sendCommand(data, lock)

    # Cleanup
    clientThread.join()

