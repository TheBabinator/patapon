import lib.game
import lib.graphics
import lib.entity

class Pon(lib.entity.Entity):
    def __init__(self, control, friendly):
        super().__init__(control)
        self.friendly = friendly

    def update(self):
        pass

    def draw(self):
        x = self.x - self.control.camerax
        y = lib.game.height - (self.y - self.control.cameray)
        lib.graphics.rect((0, 0, 0), (x + 11, y - 11, 2, 11))
        lib.graphics.rect((0, 0, 0), (x + 17, y - 11, 2, 11))
        lib.graphics.rect((0, 0, 0), (x + 8, y - 2, 3, 2))
        lib.graphics.rect((0, 0, 0), (x + 19, y - 2, 3, 2))
        lib.graphics.ellipse((0, 0, 0), (x, y - 36, 30, 30))
        lib.graphics.ellipse((255, 255, 255), (x + 5, y - 36 + 5, 20, 20))
        lib.graphics.ellipse((0, 0, 0), (x + 10, y - 36 + 10, 10, 10))
