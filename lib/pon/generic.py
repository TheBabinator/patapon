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
patapon_angry = patapon_atlas.region((90, 0, 30, 30))
patapon_angry_alt = patapon_atlas.region((90, 30, 30, 30))
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
        self.hatapon = False
        self.timer = 0
        self.helmet = lib.content.accessories.content["wooden-helm"]
        self.playinganimation = "idle"
        self.animationtime = 0

    def animation(self, name):
        self.playinganimation = name
        self.animationtime = 4

    def attack(self):
        pass

    def defend(self):
        pass

    def charge(self):
        pass

    def update(self):
        if self.animationtime > 0:
            self.animationtime -= lib.game.deltatime
        else:
            self.playinganimation = "idle"
            self.animationtime = 0

    def draw(self):
        x = self.x - self.control.camerax
        y = lib.game.height - (self.y - self.control.cameray)
        y -= math.floor((self.timer % 0.5) * 6) * 2
        patapon_legs[math.floor(self.timer % 1 * 4)].draw((x, y - 30))
        self.helmet.region.draw((x, y - 60))
        patapon_head.draw((x, y - 40))
        patapon_eye.draw((x, y - 40))
        if self.playinganimation == "angry":
            patapon_pupil.draw((x + 3, y - 40))
            patapon_angry.draw((x, y - 40))
        elif self.playinganimation == "charge":
            patapon_pupil.draw((x, y - 38))
            patapon_angry_alt.draw((x, y - 40))
        elif self.playinganimation == "confused":
            patapon_pupil_alt.draw((x, y - 40))
        else:
            patapon_pupil.draw((x, y - 40))

class Hatapon(Pon):
    def __init__(self, control):
        super().__init__(control, True)
        self.hatapon = True
        self.helmet = lib.content.accessories.content["iron-helm"]

class Yaripon(Pon):
    def __init__(self, control, friendly):
        super().__init__(control, friendly)
    
    def attack(self):
        super().attack()
        self.animation("angry")

    def defend(self):
        super().defend()
        self.attack()

    def charge(self):
        super().charge()
        self.animation("charge")
