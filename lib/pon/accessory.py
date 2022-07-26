import lib.graphics

class Accessory:
    def __init__(self, name, attributes = {}):
        self.name = name
        self.attributes = attributes
        self.region = lib.graphics.Atlas("assets/sprites/entity/pon/accessory/" + name + ".png").region((0, 0, 30, 30))
