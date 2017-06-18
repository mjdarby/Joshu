import datetime
import time
import urllib.request
import urllib.parse
import json
import random
from enum import Enum
from .command import BaseCommand
from app.cron.cron import Cron

class WeatherCondition(Enum):
    FAIRDAY = 1
    FAIRNIGHT = 2
    HOT = 3
    CLOUDY = 4
    CLEARNIGHT = 5
    SUNNY = 6
    RAINY = 7
    HAIL = 8
    SLEET = 9
    DUST = 10
    FOG = 11
    WINDY = 12
    COLD = 13
    SNOWY = 14
    THUNDERSTORM = 15
    THUNDERSHOWER = 16
    STAYINDOORS = 17

def codeToCondition(code):
    codeToConditionMap = {0: WeatherCondition.STAYINDOORS,
                          1: WeatherCondition.STAYINDOORS,
                          2: WeatherCondition.STAYINDOORS,
                          3: WeatherCondition.THUNDERSTORM,
                          4: WeatherCondition.THUNDERSTORM,
                          37: WeatherCondition.THUNDERSTORM,
                          38: WeatherCondition.THUNDERSTORM,
                          39: WeatherCondition.THUNDERSTORM,
                          5: WeatherCondition.SNOWY,
                          7: WeatherCondition.SNOWY,
                          13: WeatherCondition.SNOWY,
                          14: WeatherCondition.SNOWY,
                          15: WeatherCondition.SNOWY,
                          16: WeatherCondition.SNOWY,
                          41: WeatherCondition.SNOWY,
                          42: WeatherCondition.SNOWY,
                          43: WeatherCondition.SNOWY,
                          46: WeatherCondition.SNOWY,
                          6: WeatherCondition.RAINY,
                          8: WeatherCondition.RAINY,
                          9: WeatherCondition.RAINY,
                          10: WeatherCondition.RAINY,
                          11: WeatherCondition.RAINY,
                          12: WeatherCondition.RAINY,
                          40: WeatherCondition.RAINY,
                          33: WeatherCondition.FAIRDAY,
                          34: WeatherCondition.FAIRNIGHT,
                          36: WeatherCondition.HOT,
                          26: WeatherCondition.CLOUDY,
                          27: WeatherCondition.CLOUDY,
                          28: WeatherCondition.CLOUDY,
                          29: WeatherCondition.CLOUDY,
                          30: WeatherCondition.CLOUDY,
                          44: WeatherCondition.CLOUDY,
                          31: WeatherCondition.CLEARNIGHT,
                          32: WeatherCondition.SUNNY,
                          17: WeatherCondition.HAIL,
                          35: WeatherCondition.HAIL,
                          18: WeatherCondition.SLEET,
                          19: WeatherCondition.DUST,
                          20: WeatherCondition.FOG,
                          21: WeatherCondition.FOG,
                          22: WeatherCondition.FOG,
                          23: WeatherCondition.WINDY,
                          24: WeatherCondition.WINDY,
                          25: WeatherCondition.COLD,
                          45: WeatherCondition.THUNDERSHOWER,
                          47: WeatherCondition.THUNDERSHOWER}
    return codeToConditionMap[code]

def getClientLocation(ip):
    print(ip)
    if ip == "127.0.0.1":
        ip = ""
    geoIp = urllib.request.urlopen('http://freegeoip.net/json/' + ip)
    response = geoIp.read().decode('utf-8')
    location = json.loads(response)
    print(location)
    geoIp.close()
    fullLocation = "{}, {}, {}".format(location['city'], location['region_name'], location['country_name'])
    return fullLocation

def getWeatherForLocation(location):
    yahooQuery = "select * from weather.forecast where woeid in (select woeid from geo.places(1) where text=\"{}\")".format(location)
    yahooUrl = "https://query.yahooapis.com/v1/public/yql?"
    yahooDict = {"format": "json",
                 "env": "http://datatables.org/alltables.env",
                 "q": yahooQuery,
                 "callback": "YUI.Env.JSONP.yui_3_17_2_1_1497785521566_577"}
    yahooUrl += urllib.parse.urlencode(yahooDict)
    yahooRequest = urllib.request.urlopen(yahooUrl)
    yahooResponse = yahooRequest.read().decode('utf-8')[49:-2]
    yahooJson = json.loads(yahooResponse)
    print(json.dumps(yahooJson, indent=4))
    return yahooJson

def processJsonToResponse(yahooJson):
    response = ""
    # From the Yahoo API docs
    currentCondition = codeToCondition(int(yahooJson["query"]["results"]["channel"]["item"]["condition"]["code"]))
    if currentCondition == WeatherCondition.FAIRDAY:
        response = random.choice(["It's looking nice out!"])
    elif currentCondition == WeatherCondition.FAIRNIGHT:
        response = random.choice(["Might be a nice night for a walk."])
    elif currentCondition == WeatherCondition.HOT:
        response = random.choice(["Phew, it's warm out! Maybe leave the jacket."])
    elif currentCondition == WeatherCondition.CLOUDY:
        response = random.choice(["It's cloudy out. At least it's not raining."])
    elif currentCondition == WeatherCondition.CLEARNIGHT:
        response = random.choice(["Not a cloud in the sky, maybe we could take a walk?"])
    elif currentCondition == WeatherCondition.SUNNY:
        response = random.choice(["Put on some sunscreen and enjoy the day."])
    elif currentCondition == WeatherCondition.RAINY:
        response = random.choice(["Grab an umbrella if you're going out, it's raining."])
    elif currentCondition == WeatherCondition.HAIL:
        response = random.choice(["I don't like hail... It hurts! And also, that's what's happening right now."])
    elif currentCondition == WeatherCondition.SLEET:
        response = random.choice(["Pretty sleety today. Be careful."])
    elif currentCondition == WeatherCondition.DUST:
        response = random.choice(["It's so dusty out..! You should keep your eyes covered."])
    elif currentCondition == WeatherCondition.FOG:
        response = random.choice(["Can't see much, there's a lot of fog. Be careful, okay?"])
    elif currentCondition == WeatherCondition.WINDY:
        response = random.choice(["Hold on to your hat, there's a breeze going on out there."])
    elif currentCondition == WeatherCondition.COLD:
        response = random.choice(["Brrr, you should grab a coat. It's chilly out!"])
    elif currentCondition == WeatherCondition.SNOWY:
        response = random.choice(["Do you wanna build a snowman? 'cause if the snow outside settles, we totally can!"])
    elif currentCondition == WeatherCondition.THUNDERSTORM:
        response = random.choice(["Wow, thunder and lightning! I wouldn't go out if I could help it."])
    elif currentCondition == WeatherCondition.THUNDERSHOWER:
        response = random.choice(["Thunder, lightning, and even rain to boot!"])
    elif currentCondition == WeatherCondition.STAYINDOORS:
        response = random.choice(["It's really scary out, you should be careful, okay?"])

    forecastCondition = yahooJson["query"]["results"]["channel"]["item"]["forecast"][0]
    # Check forecast is for today
    forecastDate = datetime.datetime.strptime(forecastCondition["date"], '%d %b %Y')
    if (forecastDate.date() == datetime.datetime.today().date()):
        forecastCondition = codeToCondition(int(forecastCondition["code"]))
        response += " "
        if forecastCondition == currentCondition:
            pass
        elif forecastCondition == WeatherCondition.FAIRDAY or forecastCondition == WeatherCondition.FAIRNIGHT or forecastCondition == WeatherCondition.CLEARNIGHT:
            response += random.choice(["Later on, it'll be good walking weather."])
        elif forecastCondition == WeatherCondition.FAIRNIGHT:
            response += random.choice(["Should turn out to be a nice night too.."])
        elif forecastCondition == WeatherCondition.RAINY:
            response += random.choice(["But later on I think it's going to rain, so you should take an umbrella with you."])
        elif forecastCondition == WeatherCondition.HAIL:
            response += random.choice(["Gonna turn haily later. Cover up!"])
        elif forecastCondition == WeatherCondition.SLEET:
            response += random.choice(["Watch out for the sleet later on."])
        elif forecastCondition == WeatherCondition.COLD:
            response += random.choice(["It'll be cold later, so take a coat."])
        elif forecastCondition == WeatherCondition.SNOWY:
            response += random.choice(["It might snow later, so wear good shoes!"])
        elif forecastCondition == WeatherCondition.THUNDERSTORM or forecastCondition == WeatherCondition.THUNDERSHOWER:
            response += random.choice(["It's going to be stormy later, so stay safe."])
        elif forecastCondition == WeatherCondition.STAYINDOORS:
            response += random.choice(["It's gonna get scary out later, so stay safe, okay?"])
    return response

class Weather(BaseCommand):
    def __init__(self, dataStore):
        super(Weather, self).__init__("weather")
        self.dataStore = dataStore

    def run(self, connectionInfo, slots):
        location = ""

        if len(slots) > 0:
            location = slots[0]
        else:
            location = getClientLocation(connectionInfo.ip)

        yahooJson = getWeatherForLocation(location)
        response = processJsonToResponse(yahooJson)

        return response
