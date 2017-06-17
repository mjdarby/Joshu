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
Creates a cronjob (implemented) to tell server to run wakeUp (implemented) and send to attached clients
### Parameters
* Alarm time as unix timestamp
## wakeUp
Tells server to send 'wakey-wakey' (implemented) to all attached clients
Enhancement: Only target clients for which we set an alarm for
Enhancement: Re-enqueue self until 'awake' signal received
