import pygame
import lib.game

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

