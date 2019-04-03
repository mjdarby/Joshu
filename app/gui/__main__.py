import pygame
import sys
import os
import glob
import app.speechrecog.speech
import pyaudio
from threading import RLock, Thread
from app.shared.response import Response
from app.client.client import runClientThread, sendCommand
from app.hotword.hotword import runHotwordThread
from app.speechsynth import voice
from json import JSONDecodeError

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../Porcupine/binding/python'))
from porcupine import Porcupine

size = width, height = 640, 480
black = 0,0,0

class AnimationFrames():
    def __init__(self):
        self.surfaces = []
        self.frameCount = 0
        self.framerate = 30
        self.timeToNextFrame = self.framerate
        self.currentFrame = 0
        self.frameToLoopFrom = 1
        self.playing = False

    def loadAnimation(self, baseFilename):
        filenames = glob.glob("app/gui/assets/{}*.png".format(baseFilename))
        filenames.sort()
        for filename in filenames:
            newSurface = pygame.image.load(filename)
            newSurface = pygame.transform.smoothscale(newSurface, (243, 432))
            self.surfaces.append(newSurface)
            self.frameCount = len(self.surfaces)

    def advanceAnimation(self):
        if self.playing:
            if self.timeToNextFrame <= 0:
                self.timeToNextFrame = self.framerate
                self.currentFrame += 1
                if self.currentFrame >= self.frameCount:
                    self.currentFrame = self.frameToLoopFrom
            else:
                self.timeToNextFrame -= 1

    def playAnimation(self):
        self.playing = True
        self.currentFrame = 1

    def stopAnimation(self):
        self.playing = False

    def resetAnimation(self):
        self.stopAnimation()
        self.currentFrame = 0

    def getDisplaySurface(self):
        return self.surfaces[self.currentFrame]

class Character():
    def __init__(self):
        self.animations = {}
        self.currentAnimation = "neutral"
        self.timeToNeutral = -1
        self.timeToWaitBeforeNeutral = 120

    def loadAssets(self):
        moods = ["annoyed", "angry", "neutral", "happy"]
        for mood in moods:
            animation = AnimationFrames()
            animation.loadAnimation(mood)
            self.animations[mood] = animation

    def logic(self):
        if self.timeToNeutral == 0 and not self.animations[self.currentAnimation].playing:
            self.currentAnimation = "neutral"
            self.resetAnimation()
            self.timeToNeutral = -1 # Who wants to reason about threads anyway?
        elif self.timeToNeutral > 0:
            self.timeToNeutral -= 1
        self.animations[self.currentAnimation].advanceAnimation()

    def setAnimation(self, animationName):
        self.currentAnimation = animationName

    def playAnimation(self):
        self.animations[self.currentAnimation].playAnimation()

    def stopAnimation(self):
        self.animations[self.currentAnimation].stopAnimation()

    def resetAnimation(self):
        self.timeToNeutral = self.timeToWaitBeforeNeutral
        self.animations[self.currentAnimation].resetAnimation()

    def getDisplaySurface(self):
        return self.animations[self.currentAnimation].getDisplaySurface()


def voiceResponse(text, mood, character):
    voiceThread = Thread(None, target=_voiceResponse, args=(text, mood, character))
    voiceThread.start()

def _voiceResponse(text, mood, character):
    character.setAnimation(mood)
    character.playAnimation()
    voice.speak(text)
    character.resetAnimation()

def processCommand(server, clientThread, host, string, character):
    if (string == "quit"):
        server.shutdown()
        clientThread.join()
        sys.exit()
    else:
        received = sendCommand(host, string, lock)
        processResponse(received)

def processResponse(json):
    try:
        response = Response.decodeJson(json)
        voiceResponse(response.text, response.mood, character)
    except JSONDecodeError:
        voiceResponse("Oops, something went wrong.", "neutral", character)

def renderBackground(screen):
    screen.fill(black)

def renderCharacter(character, screen):
    surfaceToRender = character.getDisplaySurface()
    screen.blit(surfaceToRender, (width / 2 - surfaceToRender.get_width() / 2, 0))

def renderText(inputString, surface):
    textSurface = pygameFont.render(">" + inputString, True, (255,255,255))
    screen.blit(textSurface, (0, height - pygameFont.size(inputString)[1]))

if __name__ == "__main__":
    host = sys.argv[1]

    # Pygame setup
    pygame.init()
    pygame.display.set_caption("Joshu v0.1c: Stronger Moments")

    screen = pygame.display.set_mode(size)

    clock = pygame.time.Clock()
    pygameFont = pygame.font.SysFont('Consolas', 16)

    # Load assets
    character = Character()
    character.loadAssets()

    # Get the hotword and threads out of the way
    porcupine = Porcupine(
        library_path=os.path.join(os.path.dirname(__file__), '../../../../Porcupine/lib/linux/x86_64/libpv_porcupine.so'),
        model_file_path=os.path.join(os.path.dirname(__file__), '../../../../Porcupine/lib/common/porcupine_params.pv'),
        keyword_file_paths=[os.path.join(os.path.dirname(__file__), '../../assistant_linux.ppn')],
        sensitivities=[0.5])

    pa = pyaudio.PyAudio()
    audio_stream = pa.open(
        rate=porcupine.sample_rate,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=porcupine.frame_length,
        input_device_index=None)

    def callback(data):
        processResponse(data)

    def hotwordCallback():
#        ping = pygame.mixer.Sound('ping.wav')
#        ping.play()
#        voiceResponse("Yes?", "neutral", character)
        valid, string, slots = app.speechrecog.speech.getAudio(porcupine, pa, audio_stream)
        if valid:
            processCommand(server, clientThread, host, string, character)
        else:
            voiceResponse(string, "neutral", character)

    # Setup
    lock = RLock()
    clientThread, server = runClientThread(lock, callback)
    inputString = ""

    hotwordThread = runHotwordThread(hotwordCallback, porcupine, pa, audio_stream)

    # Main loop
    while True:
        # Regulate FPS
        time = clock.tick(60)

        # Run logic
        character.logic()

        # Process input
        keys = pygame.key.get_pressed()
        shifted = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                server.shutdown()
                clientThread.join()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                keyValue = event.key
                if keyValue == pygame.K_ESCAPE:
                    server.shutdown()
                    clientThread.join()
                    sys.exit()
                if keyValue == pygame.K_RETURN:
                    processCommand(server, clientThread, host, inputString, character)
                    inputString = ""
                if keyValue >= pygame.K_a and keyValue <= pygame.K_z:
                    if shifted:
                        keyValue -= 32
                    inputString += chr(keyValue)
                if keyValue >= pygame.K_0 and keyValue <= pygame.K_9:
                    inputString += chr(keyValue)
                if keyValue == pygame.K_SPACE:
                    inputString += chr(keyValue)
                if keyValue == pygame.K_BACKSPACE:
                    inputString = inputString[0:-1]
                if keyValue == pygame.K_TAB:
                    hotwordCallback()

        # Display
        renderBackground(screen)
        renderCharacter(character, screen)
        renderText(inputString, screen)
        pygame.display.flip()
