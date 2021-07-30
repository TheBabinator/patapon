import lib.game
import lib.content.statuseffects

class Entity:
    def __init__(self, control):
        self.control = control
        self.x = 0
        self.y = 0
        self.age = 0
        self.statuseffects = []
        self.alive = True
        self.health = 100
        
    def update(self):
        for instance in self.statuseffects:
            instance.update(self)
        if self.health <= 0:
            self.health = 0
            self.alive = False
        self.age += lib.game.deltatime
    
    def draw(self):
        pass
