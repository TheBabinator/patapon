import pygame

bindings = {}
states = {}

def addkey(name, keys):
    bindings[name] = keys
    states[name] = [False, False, False, 0]

def getkey(binding):
    return states[binding]

def update():
    pressed = pygame.key.get_pressed()
    for name, keys in bindings.items():
        down = False
        for key in keys:
            if pressed[key]:
                down = True
        state = states[name]
        if down:
            state[0] = True
            if state[3] == 0:
                state[1] = True
            else:
                state[1] = False
            state[2] = False
            state[3] += 1
        else:
            state[0] = False
            state[1] = False
            if state[3] != 0:
                state[2] = True
            else:
                state[2] = False
            state[3] = 0
            

addkey("square", [pygame.K_LEFT])
addkey("circle", [pygame.K_RIGHT])
addkey("cross", [pygame.K_DOWN])
addkey("triangle", [pygame.K_UP])
