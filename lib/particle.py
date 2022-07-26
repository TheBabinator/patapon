import random
import math
import lib.game
import lib.graphics
import lib.entity

class Particle(lib.entity.Entity):
    def __init__(self, control):
        super().__init__(control)
        self.invulnerable = True
        self.lifetime = 1
    
    def update(self):
        super().update()
        if self.age > self.lifetime:
            self.control.entities.remove(self)
    
    def draw(self):
        x = self.x - self.control.camerax
        y = lib.game.height - (self.y - self.control.cameray)
        return x, y

statusparticle_atlas = lib.graphics.Atlas("assets/sprites/fx/status.png")
statusparticle_style = []
for x in range(2):
    frames = []
    for y in range(4):
        frames.append(statusparticle_atlas.region((x * 15, y * 15, 15, 15)))
    statusparticle_style.append(frames)

class StatusParticle(Particle):
    def __init__(self, control, style):
        super().__init__(control)
        self.lifetime = 0.25
        self.style = random.choice(statusparticle_style[style])
    
    def update(self):
        super().update()
    
    def draw(self):
        x, y = super().draw()
        self.style.draw((x, y))

damagetext_atlas = lib.graphics.Atlas("assets/sprites/fx/damagetext.png")
damagetext = []
for x in range(10):
    damagetext.append(damagetext_atlas.region((x * 25, 25, 25, 25)))
damagetext_alt = []
for x in range(10):
    damagetext_alt.append(damagetext_atlas.region((x * 25, 0, 25, 25)))

class DamageIndicatorParticle(Particle):
    def __init__(self, control):
        super().__init__(control)
        self.lifetime = 2
        self.damaged = 0
        self.critical = False
        
        self.ax = random.randint(-100, 100)
        self.ay = random.randint(0, 100)
    
    def update(self):
        super().update()
        if self.age < 0.5:
            self.ay -= 500 * lib.game.deltatime
            self.ax -= self.ax * 0.1 * lib.game.deltatime
            self.ay -= self.ax * 0.1 * lib.game.deltatime
        else:
            self.ax -= self.ax * 10 * lib.game.deltatime
            self.ay = 0
        self.x += self.ax * lib.game.deltatime
        self.y += self.ay * lib.game.deltatime

    def draw(self):
        x, y = super().draw()
        string = str(math.ceil(self.damaged))
        for digit in string:
            number = int(digit)
            if self.critical:
                damagetext_alt[number].draw((x, y))
            else:
                damagetext[number].draw((x, y))
            x += 20
