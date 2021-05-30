import lib.game

class Entity:
    def __init__(self, control):
        self.control = control
        self.x = 0
        self.y = 0
        self.age = 0
        
    def update(self):
        self.age += lib.game.deltatime
    
    def draw(self):
        pass
