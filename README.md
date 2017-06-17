# Joshu
An experiment in doing something a bit Alexa-y

# Usage
Joshu is written in Python 3
## Run server
    python -m app.server

## Run text client
    python -m app.client <command> <parameters>

# Commands
## setAlarm
Creates a cronjob (implemented) to tell server to run wakeUp (implemented) and send to attached clients (not implemented)
### Parameters
* Alarm time as unix timestamp
## wakeUp
Tells server to send 'wakey-wakey' (implemented) to attached clients (not implemented)
