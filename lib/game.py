import sys
import pygame
import lib.graphics
import lib.data.mission
import lib.input
import lib.control

width = 1280
height = 720
targetfps = 120
frame = 0
deltatime = 0
tickslastframe = 0

screen = None

mission = None 
control = None

def close():
    pygame.quit()
    sys.exit()

def update():
    global control

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            close()
    
    lib.input.update()
    control.update()

def draw():
    global screen
    global control

    screen.fill((0, 0, 0))

    control.draw()
    
    pygame.display.flip()

def launch(track):
    global targetfps
    global frame
    global deltatime
    global tickslastframe
    global screen
    global mission
    global control
    
    pygame.init()
    pygame.mixer.init(frequency = 44100, channels = 16)
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("PATAPON 4: MEDEN FUCKING DIES (AGAIN)")
    pygame.display.set_icon(pygame.image.load("assets/icon.png"))

    mission = lib.data.mission.Mission(track)
    control = lib.control.Control(mission)

    clock = pygame.time.Clock()
    while True:
        frame += 1
        t = pygame.time.get_ticks()
        deltatime = (t - tickslastframe) / 1000 
        update()
        draw()
        tickslastframe = t
        clock.tick(targetfps)
