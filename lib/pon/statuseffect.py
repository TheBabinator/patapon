import random
import lib.game
import lib.content.statuseffects

class StatusEffectEntity:
    def __init__(self, name):
        self.name = name
        self.effect = lib.content.statuseffects.content[self.name]
        self.timer = 0
    
    def update(self, entity):
        if self.timer <= 0:
            damage = random.randint(self.effect.attributes["damageMin"], self.effect.attributes["damageMax"])
            entity.health = entity.health - damage
            self.timer = self.effect.attributes["damageTime"]
        self.timer -= lib.game.deltatime

class StatusEffect:
    def __init__(self, name, attributes):
        self.name = name
        self.attributes = attributes

    def give(self, entity):
        for instance in entity.statuseffects:
            if instance.name == self.name:
                return
        instance = StatusEffectEntity(self.name)
        instance.timer = self.attributes["damageTime"]
        entity.statuseffects.append(instance)
