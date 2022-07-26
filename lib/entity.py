import lib.game
import lib.content.statuseffects

class Entity:
    def __init__(self, control):
        self.control = control
        self.x = 0
        self.y = 0
        self.age = 0
        self.invulnerable = False
        self.statuseffects = []
        self.alive = True
        self.health = 100
        
        self.control.entities.append(self)
        
    def update(self):
        if not self.invulnerable:
            for instance in self.statuseffects:
                instance.update(self)
            if self.health <= 0:
                self.statuseffects = []
                self.health = 0
                self.alive = False
        self.age += lib.game.deltatime
    
    def draw(self):
        pass

    def damage(self, amount, critical = False):
        import lib.particle

        self.health -= amount
        particle = lib.particle.DamageIndicatorParticle(self.control)
        particle.x = self.x + 5
        particle.y = self.y + 45
        particle.damaged = amount
        particle.critical = critical
