import pygame

sounds = {}

def preload(name, file):
    if not name in sounds:
        sound = pygame.mixer.Sound(file)
        sounds[name] = sound

def unload(name):
    if name in sounds:
        sounds[name] = None

def getc(channel):
    return pygame.mixer.Channel(channel)

def play(channel, name, volume = 1):
    c = getc(channel)
    if name in sounds:
        sound = sounds[name]
        c.play(sound)
        c.set_volume(volume)

def stop(channel):
    c = getc(channel)
    c.stop()
