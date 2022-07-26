import random
import lib.game
import lib.content.statuseffects

class StatusEffectEntity:
    def __init__(self, name):
        self.name = name
        self.effect = lib.content.statuseffects.content[self.name]
        self.timer = 0
        self.particletimer = 0
    
    def update(self, entity):
        import lib.particle
        import lib.game

        if self.timer <= 0:
            if random.random() >= self.effect.attributes["critChance"]:
                damage = random.randint(self.effect.attributes["damageMin"], self.effect.attributes["damageMax"])
                entity.damage(damage)
            else:
                damage = random.randint(self.effect.attributes["damageMin"], self.effect.attributes["damageMax"])
                entity.damage(damage * self.effect.attributes["critMult"], critical = True)
            self.timer = self.effect.attributes["damageTime"]
        if self.particletimer <= 0:
            particle = lib.particle.StatusParticle(entity.control, self.effect.attributes["particle"])
            particle.x = entity.x + random.randint(-5, 20)
            particle.y = entity.y + random.randint(5, 50)
            self.particletimer = 0.125
        self.timer -= lib.game.deltatime
        self.particletimer -= lib.game.deltatime

class StatusEffect:
    def __init__(self, name, attributes):
        self.name = name
        self.attributes = attributes

    def give(self, entity):
        if entity.alive:
            for instance in entity.statuseffects:
                if instance.name == self.name:
                    return
            instance = StatusEffectEntity(self.name)
            instance.timer = self.attributes["damageTime"]
            entity.statuseffects.append(instance)
