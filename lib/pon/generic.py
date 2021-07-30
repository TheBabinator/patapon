import math
import random
import lib.game
import lib.graphics
import lib.entity
import lib.math2
import lib.content.accessories
import lib.content.statuseffects

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
    patapon_atlas.region((30, 60, 30, 30)),
]
patapon_legs_alt = [
    patapon_atlas.region((0, 90, 30, 30)),
    patapon_atlas.region((30, 90, 30, 30)),
    patapon_atlas.region((0, 120, 30, 30)),
    patapon_atlas.region((30, 120, 30, 30)),
]
hatapon_atlas = lib.graphics.Atlas("assets/sprites/entity/pon/hatapon.png")
hatapon_arms_normal = hatapon_atlas.region((0, 0, 50, 50))
hatapon_arms_up = hatapon_atlas.region((50, 0, 50, 50))
hatapon_flagpole = hatapon_atlas.region((100, 0, 50, 150))
hatapon_flag = hatapon_atlas.region((0, 50, 50, 100))
yaripon_atlas = lib.graphics.Atlas("assets/sprites/entity/pon/yaripon.png")
yaripon_arms_normal = yaripon_atlas.region((0, 0, 50, 50))
yaripon_arms_ready = yaripon_atlas.region((50, 0, 50, 50))
yaripon_arms_charge = yaripon_atlas.region((100, 0, 50, 50))
yaripon_arms_alt = [
    yaripon_atlas.region((0, 50, 50, 50)),
    yaripon_atlas.region((50, 50, 50, 50)),
    yaripon_atlas.region((0, 100, 50, 50)),
    yaripon_atlas.region((50, 100, 50, 50)),
]

class Pon(lib.entity.Entity):
    def __init__(self, control, friendly):
        super().__init__(control)
        self.friendly = friendly
        self.hatapon = False
        self.timer = 0
        self.helmet = lib.content.accessories.content["wooden-helm"]
        self.weapon = None
        self.playinganimation = "idle"
        self.animationtime = 0
        self.markeroffset = 0
        self.moving = False
        self.movetarget = 0
        self.movespeed = 0

    def animation(self, name, time = 2):
        self.playinganimation = name
        self.animationtime = time
    
    def march(self, marker, speed):
        self.moving = True
        self.movetarget = marker + self.markeroffset
        self.movespeed = speed
        self.animation("idle")

    def attack(self):
        self.animation("idle")

    def defend(self):
        self.animation("idle")

    def charge(self):
        self.animation("idle")

    def party(self):
        self.statuseffects = []
        self.animation("idle")

    def update(self):
        super().update()
        if self.animationtime > 0:
            self.animationtime -= lib.game.deltatime
        else:
            self.playinganimation = "idle"
            self.animationtime = 0
        if self.moving:
            if random.randint(1, 1000) == 1:
                lib.content.statuseffects.content["burn"].give(self)
            if self.x < self.movetarget:
                self.x = min(self.x + self.movespeed * lib.game.deltatime, self.movetarget)
            elif self.x > self.movetarget:
                self.x = max(self.x - self.movespeed * lib.game.deltatime, self.movetarget)
            else:
                self.moving = False

    def drawAt(self, x, y, ry):
        if self.playinganimation == "pata":
            t = max((self.animationtime - 0.25) * 2, 0)
            patapon_legs_alt[0].draw((x, ry - 30))
            y = ry - 2 * lib.math2.bias(t, 5)
            x = x - 3 * lib.math2.bias(t, 2)
        elif self.playinganimation == "pon":
            t = max((self.animationtime - 0.25) * 2, 0)
            patapon_legs_alt[1].draw((x, ry - 30))
            y = ry - 2 * lib.math2.bias(t, 5)
            x = x + 3 * lib.math2.bias(t, 2)
        elif self.playinganimation == "don":
            t = max((self.animationtime - 0.25) * 2, 0)
            patapon_legs_alt[2].draw((x, ry - 30))
            y = ry + 4 * lib.math2.bias(t, 5)
        elif self.playinganimation == "chaka":
            t = max((self.animationtime - 0.25) * 2, 0)
            patapon_legs_alt[3].draw((x, ry - 30))
            y = ry - 4 * lib.math2.bias(t, 5)
        else:
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
        elif self.playinganimation == "pata":
            t = max((self.animationtime - 0.25) * 2, 0)
            m = lib.math2.bias(t, 0.2)
            patapon_pupil.draw((x - 3 * m, y - 40 - 2 * m))
        elif self.playinganimation == "pon":
            t = max((self.animationtime - 0.25) * 2, 0)
            m = lib.math2.bias(t, 0.2)
            patapon_pupil.draw((x + 3 * m, y - 40 - 2 * m))
        elif self.playinganimation == "don":
            t = max((self.animationtime - 0.25) * 2, 0)
            m = lib.math2.bias(t, 0.2)
            patapon_pupil.draw((x, y - 40 + 4 * m))
        elif self.playinganimation == "chaka":
            t = max((self.animationtime - 0.25) * 2, 0)
            m = lib.math2.bias(t, 0.2)
            patapon_pupil.draw((x, y - 40 - 4 * m))
        else:
            patapon_pupil.draw((x, y - 40))
        return x, y

    def draw(self):
        if self.alive:
            x = self.x - self.control.camerax
            ry = lib.game.height - (self.y - self.control.cameray)
            y = ry
            y -= math.floor((self.timer % 0.5) * 6) * 2
            return self.drawAt(x, y, ry)
    
    def drawPreview(self, x, y):
        ry = y
        y -= math.floor((self.timer % 0.5) * 6) * 2
        self.drawAt(x, y, ry)

class Hatapon(Pon):
    def __init__(self, control):
        super().__init__(control, True)
        self.hatapon = True
        self.helmet = lib.content.accessories.content["iron-helm"]
    
    def drawAt(self, x, y, ry):
        super().drawAt(x, y, ry)
        if not self.moving:
            hatapon_arms_normal.draw((x - 10, y - 50))
            hatapon_flagpole.draw((x - 8, y - 155))
            hatapon_flag.draw((x - 8, y - 120))
        else:
            hatapon_arms_up.draw((x - 10, y - 50))
            hatapon_flagpole.draw((x - 10, y - 195))
            hatapon_flag.draw((x - 10, y - 160))

class Yaripon(Pon):
    def __init__(self, control, friendly):
        super().__init__(control, friendly)
        self.weapon = lib.content.accessories.content["wooden-spear"]
    
    def drawAt(self, x, y, ry):
        x, y = super().drawAt(x, y, ry)
        if self.playinganimation == "charge":
            yaripon_arms_charge.draw((x - 10, y - 50))
        elif self.playinganimation == "pata":
            yaripon_arms_alt[0].draw((x - 10, y - 50))
        elif self.playinganimation == "pon":
            yaripon_arms_alt[1].draw((x - 10, y - 50))
        elif self.playinganimation == "don":
            yaripon_arms_alt[2].draw((x - 10, y - 50))
        elif self.playinganimation == "chaka":
            yaripon_arms_alt[3].draw((x - 10, y - 50))
        else:
            yaripon_arms_normal.draw((x - 10, y - 50))

    def attack(self):
        super().attack()
        self.animation("angry")

    def defend(self):
        super().defend()
        self.attack()

    def charge(self):
        super().charge()
        self.animation("charge")
