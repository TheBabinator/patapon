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

pygame.init()
pygame.mixer.init(frequency = 44100, channels = 16)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("patapon 4 or something")
pygame.display.set_icon(pygame.image.load("assets/icon.png"))

mission = lib.data.mission.Mission("freakout-rock")
test = lib.control.Control(mission)

def close():
    pygame.quit()
    sys.exit()

def update():
    global test

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            close()
    
    lib.input.update()
    test.update()

def draw():
    global screen
    global test

    screen.fill((0, 0, 0))

    test.draw()
    
    pygame.display.flip()

def launch():
    global targetfps
    global frame
    global deltatime
    global tickslastframe

    clock = pygame.time.Clock()
    while True:
        frame += 1
        t = pygame.time.get_ticks()
        deltatime = (t - tickslastframe) / 1000 
        update()
        draw()
        tickslastframe = t
        clock.tick(targetfps)
