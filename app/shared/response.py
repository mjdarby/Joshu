import json

class Response():
    def __init__(self, text, mood):
        self.text = text
        self.mood = mood

    def getJson(self):
        responseObject = {}
        responseObject["text"] = self.text
        responseObject["mood"] = self.mood
        return json.dumps(responseObject)

    def decodeJson(jsonString):
        responseObject  = json.loads(jsonString)
        return Response(responseObject["text"], responseObject["mood"])
