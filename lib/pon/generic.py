import math
import lib.game
import lib.graphics
import lib.entity
import lib.content.accessories

patapon_atlas = lib.graphics.Atlas("assets/sprites/entity/pon/patapon.png")
patapon_head = patapon_atlas.region((0, 0, 30, 30))
patapon_eye = patapon_atlas.region((30, 0, 30, 30))
patapon_pupil = patapon_atlas.region((60, 0, 30, 30))
patapon_pupil_alt = patapon_atlas.region((60, 30, 30, 30))
patapon_legs = [
    patapon_atlas.region((0, 30, 30, 30)),
    patapon_atlas.region((30, 30, 30, 30)),
    patapon_atlas.region((0, 60, 30, 30)),
    patapon_atlas.region((30, 60, 30, 30))
]

class Pon(lib.entity.Entity):
    def __init__(self, control, friendly):
        super().__init__(control)
        self.friendly = friendly
        self.timer = 0
        self.helmet = lib.content.accessories.content["iron-helm"]
    
    def update(self):
        pass

    def draw(self):
        x = self.x - self.control.camerax
        y = lib.game.height - (self.y - self.control.cameray)
        y -= math.floor((self.timer % 0.5) * 6) * 2
        patapon_legs[math.floor(self.timer % 1 * 4)].draw((x, y - 30))
        self.helmet.region.draw((x, y - 60))
        patapon_head.draw((x, y - 40))
        patapon_eye.draw((x, y - 40))
        patapon_pupil.draw((x, y - 40))
