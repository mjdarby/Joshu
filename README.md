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
Creates a cronjob to tell server to run wakeUp and send to attached clients
### Parameters
* Alarm time as unix timestamp
## wakeUp
Debug client only, should only be used as part of Cron job
Tells server to send 'wakey-wakey' (implemented) to all attached clients. Re-enqueues self if 'awake' command not issued.
Enhancement: Only target clients for which we set an alarm for
## awake
Tells Joshu to stop the alarm if it's running, otherwise responds with an acknowledgement
## weather
If given a location name, retrieves and reports the weather there.
Otherwise tries to report the weather data for the client's location.

# Requirements
* Python 3.6.1 or greater
* Porcupine installed and the relevant parameters set in the config file
* pip modules:
    * Check out requirements.txt
* A set of ordered animation frames in app/gui/assets (for using the 'gui')
    * Frame 0 should have no mouth movement
    * Hardcoded at 3 fps
    * Base filenames must be after the moods returned by server, like:
        * annoyed1.png, annoyed2.png, annoyed3.png
    * Current moods are:
        * "annoyed"
        * "neutral"
        * "happy"
* Currently, using the graphical GUI requires an Amazon AWS account - setup instructions to come