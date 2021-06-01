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
hatapon_atlas = lib.graphics.Atlas("assets/sprites/entity/pon/hatapon.png")
hatapon_arms_normal = hatapon_atlas.region((0, 0, 50, 50))
hatapon_arms_up = hatapon_atlas.region((50, 0, 50, 50))
hatapon_flagpole = hatapon_atlas.region((100, 0, 50, 150))
hatapon_flag = hatapon_atlas.region((0, 50, 50, 100))

class Pon(lib.entity.Entity):
    def __init__(self, control, friendly):
        super().__init__(control)
        self.friendly = friendly
        self.hatapon = False
        self.timer = 0
        self.helmet = lib.content.accessories.content["wooden-helm"]
        self.playinganimation = "idle"
        self.animationtime = 0
        self.markeroffset = 0
        self.moving = False
        self.movetarget = 0
        self.movespeed = 0

    def animation(self, name):
        self.playinganimation = name
        self.animationtime = 4
    
    def march(self, marker, speed):
        self.moving = True
        self.movetarget = marker + self.markeroffset
        self.movespeed = speed

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
        if self.moving:
            if self.x < self.movetarget:
                self.x = min(self.x + self.movespeed * lib.game.deltatime, self.movetarget)
            elif self.x > self.movetarget:
                self.x = max(self.x - self.movespeed * lib.game.deltatime, self.movetarget)
            else:
                self.moving = False

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
    
    def draw(self):
        super().draw()
        x = self.x - self.control.camerax
        y = lib.game.height - (self.y - self.control.cameray)
        y -= math.floor((self.timer % 0.5) * 6) * 2
        if not self.moving:
            hatapon_arms_normal.draw((x - 10, y - 50))
            hatapon_flagpole.draw((x - 8, y - 155))
            hatapon_flag.draw((x - 8, y - 110))
        else:
            hatapon_arms_up.draw((x - 10, y - 50))
            hatapon_flagpole.draw((x - 10, y - 185))
            hatapon_flag.draw((x - 10, y - 140))

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
