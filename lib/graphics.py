import pygame
import lib.game

class Region:
    def __init__(self, surface):
        self.surface = surface
    
    def draw(self, position, size = None, dest = None):
        if dest == None:
            dest = lib.game.screen
        if size == None:
            rect = self.surface.get_rect()
            rect.topleft = position[0], position[1]
            dest.blit(self.surface, rect)
        else:
            size = (abs(size[0]), abs(size[1]))
            rect = self.surface.get_rect()
            rect.topleft = position[0], position[1]
            tempsurface = pygame.transform.flip(self.surface, size[0] < 0, size[1] < 0)
            tempsurface = pygame.transform.scale(tempsurface, size)
            dest.blit(tempsurface, rect)

class Atlas:
    def __init__(self, filename):
        self.sheet = pygame.image.load(filename)

    def region(self, rectangle):
        rect = pygame.Rect(rectangle)
        surface = pygame.Surface(rect.size, pygame.SRCALPHA)
        surface.blit(self.sheet, (0, 0), rect)
        new = Region(surface)
        return new

def lerp(a, b, alpha):
    return a + (b - a) * alpha

def sig(x):
    if x < -100:
        return 0
    elif x > 100:
        return 1
    else:
        return 1 / (1 + (2.714 ** -x))

def rect(color, rectangle, alpha = 1):
    if alpha == 1:
        rect = pygame.Rect(rectangle)
        surface = pygame.Surface(rect.size)
        surface.fill(color)
        lib.game.screen.blit(surface, rect)
    else:
        rect = pygame.Rect(rectangle)
        surface = pygame.Surface(rect.size, pygame.SRCALPHA)
        surface.fill(color)
        surface.set_alpha(alpha * 255)
        lib.game.screen.blit(surface, rect)

def ellipse(color, rectangle):
    pygame.draw.ellipse(lib.game.screen, color, rectangle)

