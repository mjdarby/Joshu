import pygame, sys
from threading import RLock
from app.client.client import runClientThread, sendCommand

if __name__ == "__main__":
    # Pygame setup
    pygame.init()

    size = width, height = 640, 480
    black = 0,0,0
    screen = pygame.display.set_mode(size)

    clock = pygame.time.Clock()
    pygameFont = pygame.font.SysFont('Consolas', 16)
    
    # Setup
    lock = RLock()
    clientThread, server = runClientThread(lock)

    inputString = ""
    # Main loop
    while True:
        # Regulate FPS
        time = clock.tick(60)

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
                    sendCommand(inputString, lock)
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
        textSurface = pygameFont.render(">" + inputString, True, (255,255,255))


        # Display
        screen.fill(black)
        screen.blit(textSurface, (0, height - pygameFont.size(inputString)[1]))
        pygame.display.flip()
