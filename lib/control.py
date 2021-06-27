import os
import math
import random
import pygame
import lib.game
import lib.input
import lib.math2
import lib.graphics
import lib.sound
import lib.entity
import lib.pon.generic
import lib.settings

comboworm_atlas = lib.graphics.Atlas("assets/sprites/ui/comboworm.png")
comboworm_segments = []
comboworm_segments_fever = []
comboworm_segments_top = []
comboworm_segments_top_alt = []
comboworm_segments_back = []
for x in range(350):
    if x <= 250:
        comboworm_segments.append(comboworm_atlas.region((0, 0, 1, 100)))
    else:
        comboworm_segments.append(comboworm_atlas.region((x - 251, 0, 1, 100)))
for x in range(350):
    if x <= 250:
        comboworm_segments_fever.append(comboworm_atlas.region((100, 0, 1, 100)))
    else:
        comboworm_segments_fever.append(comboworm_atlas.region((x - 251 + 100, 0, 1, 100)))
for x in range(350):
    if x <= 250:
        comboworm_segments_top.append(comboworm_atlas.region((0, 100, 1, 100)))
    else:
        comboworm_segments_top.append(comboworm_atlas.region((x - 251, 100, 1, 100)))
for x in range(350):
    if x <= 250:
        comboworm_segments_top_alt.append(comboworm_atlas.region((100, 100, 1, 100)))
    else:
        comboworm_segments_top_alt.append(comboworm_atlas.region((x - 251 + 100, 100, 1, 100)))
for x in range(350):
    if x <= 250:
        comboworm_segments_back.append(comboworm_atlas.region((0, 200, 1, 100)))
    else:
        comboworm_segments_back.append(comboworm_atlas.region((x - 251, 200, 1, 100)))
combotext_numerals = [
    comboworm_atlas.region((15, 106, 50, 50)),
    comboworm_atlas.region((15, 106, 50, 50)),
    comboworm_atlas.region((200, 0, 50, 50)),
    comboworm_atlas.region((250, 0, 50, 50)),
    comboworm_atlas.region((200, 50, 50, 50)),
    comboworm_atlas.region((250, 50, 50, 50)),
    comboworm_atlas.region((200, 100, 50, 50)),
    comboworm_atlas.region((250, 100, 50, 50)),
    comboworm_atlas.region((200, 150, 50, 50)),
    comboworm_atlas.region((250, 150, 50, 50)),
]
combotext_numerals_top = [
    comboworm_atlas.region((115, 106, 50, 50)),
    comboworm_atlas.region((115, 106, 50, 50)),
    comboworm_atlas.region((300, 0, 50, 50)),
    comboworm_atlas.region((350, 0, 50, 50)),
    comboworm_atlas.region((300, 50, 50, 50)),
    comboworm_atlas.region((350, 50, 50, 50)),
    comboworm_atlas.region((300, 100, 50, 50)),
    comboworm_atlas.region((350, 100, 50, 50)),
    comboworm_atlas.region((300, 150, 50, 50)),
    comboworm_atlas.region((350, 150, 50, 50)),
]
combotext_combo = comboworm_atlas.region((100, 200, 200, 50))
combotext_fever = comboworm_atlas.region((100, 250, 200, 50))
songs = {}

class Song:
    def __init__(self, name, pattern):
        self.name = name
        self.pattern = pattern
        songs[self.name] = self
    
    def eval(self, match, now = 0):
        if len(match) > len(self.pattern):
            return 0, 0
        i = -1
        perfects = 0
        total = 0
        for hit in match:
            i += 1
            total += 1
            if hit[0] != self.pattern[i][0]:
                return 0, 0
            if abs(hit[1] - self.pattern[i][1]) > 0.2:
                return 0, 0
            if abs(hit[1] - self.pattern[i][1]) < 0.05:
                perfects += 1
        if len(match) != len(self.pattern):
            if now >= 0.75:
                if len(match) == 0:
                    return 0, 0
                elif now >= match[i][1] + (self.pattern[i + 1][1] - self.pattern[i][1]) + 0.25:
                    return 0, 0
            return 1, 0
        return 2, perfects / total

Song("March", [("pata", 0), ("pata", 1), ("pata", 2), ("pon", 3)])
Song("Attack", [("pon", 0), ("pon", 1), ("pata", 2), ("pon", 3)])
Song("Defend", [("chaka", 0), ("chaka", 1), ("pata", 2), ("pon", 3)])
Song("Charge", [("pon", 0), ("pon", 1), ("chaka", 2), ("chaka", 3)])
Song("Retreat", [("pon", 0), ("pata", 1), ("pon", 2), ("pata", 3)])
Song("Jump", [("don", 0), ("don", 1), ("chaka", 2), ("chaka", 3)])
Song("Party", [("pata", 0), ("pon", 1), ("don", 2), ("chaka", 3)])
Song("Summon", [("don", 0), ("don", 1), ("don", 1.5), ("don", 2.5), ("don", 3)])

class Control:
    def __init__(self, mission):
        self.mission = mission
        self.camerax = -200
        self.cameray = -200
        self.entities = []
        self.marker = 0

        self.bpm = 120
        self.paused = True
        self.time = -2.5
        self.beattime = 0
        self.beat = 0
        self.measure = 0
        self.calling = False
        self.combo = -1
        self.fever = 0
        self.fevertime = 0
        self.feverwarn = 0
        self.hits = []
        self.beginnext = False

        self.hatapon = lib.pon.generic.Hatapon(self)
        self.hatapon.markeroffset = 0
        self.hatapon.x = 0
        self.entities.append(self.hatapon)

        pon = lib.pon.generic.Yaripon(self, True)
        pon.markeroffset = 60
        pon.x = 60
        self.entities.append(pon)

        pon = lib.pon.generic.Yaripon(self, True)
        pon.markeroffset = 100
        pon.x = 100
        self.entities.append(pon)

        pon = lib.pon.generic.Yaripon(self, True)
        pon.markeroffset = 140
        pon.x = 140
        self.entities.append(pon)

        self.load()

    def load(self):
        for file in os.listdir("assets/sfx/drums"):
            name = file.split(".")[0]
            lib.sound.preload(name, "assets/sfx/drums/" + file)
        for folder in os.listdir("assets/tracks/" + self.mission.track):
            for file in os.listdir("assets/tracks/" + self.mission.track +  "/" + folder):
                name = file.split(".")[0]
                lib.sound.preload(name, "assets/tracks/" + self.mission.track +  "/" + folder + "/" + file)
        for folder in os.listdir("assets/tracks/common"):
            for file in os.listdir("assets/tracks/common/" + folder):
                name = file.split(".")[0]
                lib.sound.preload(name, "assets/tracks/common/" + folder + "/" + file)

    def unload(self):
        pass

    def fail(self):
        self.combo = -1
        self.fever = 0
        self.feverwarn = 0
        self.time = 0
        self.beattime = 0
        self.beat = -1
        self.measure = -1
        lib.sound.play(2, "Complain-0" + str(random.randint(1, 2)), lib.settings.sfxvolume)
        for entity in self.entities:
            if isinstance(entity, lib.pon.generic.Pon):
                if entity.friendly:
                    entity.moving = False
                    if not entity.hatapon:
                        entity.animation("confused")

    def drum(self, name):
        nearest = lib.math2.round(self.beattime, 0.5)
        if self.combo == -1:
            self.hits.append([name, self.beattime])
            # leaving this one in because youre not going to summon in measure 0 anyway
            if len(self.hits) > 4:
                self.hits.pop(0)
            match = None
            level = 0
            score = 0
            while len(self.hits) > 0:
                test = []
                for hit in self.hits:
                    test.append([hit[0], hit[1] - lib.math2.round(self.hits[0][1], 1)])
                for sname, song in songs.items():
                    this, perfect = song.eval(test)
                    if this > level:
                        match = sname
                        level = this
                        score = perfect
                if match:
                    break
                else:
                    self.hits.pop(0)
            if level == 0:
                lib.sound.play(1, name + "_3", lib.settings.sfxvolume)
                lib.sound.play(2, "ch_" + name + "_3", lib.settings.musicvolume)
                for entity in self.entities:
                    if isinstance(entity, lib.pon.generic.Pon):
                        entity.moving = False
                        if not entity.hatapon:
                            entity.animation("confused")
            else:
                if abs(nearest - self.beattime) < 0.05:
                    lib.sound.play(1, name, lib.settings.sfxvolume)
                    lib.sound.play(2, "ch_" + name, lib.settings.musicvolume)
                else:
                    lib.sound.play(1, name + "_2", lib.settings.sfxvolume)
                    lib.sound.play(2, "ch_" + name + "_2", lib.settings.musicvolume)
                for entity in self.entities:
                        if isinstance(entity, lib.pon.generic.Pon):
                            if entity.friendly and not entity.hatapon:
                                entity.animation(name, time = 0.75)
                if level == 2:
                    if score == 1:
                        lib.sound.play(3, "perfect", lib.settings.sfxvolume)
                    if self.beat < self.beattime:
                        self.beginnext = True
        else:
            if lib.math2.round(self.beattime, 0.5) % 8 < 4:
                self.fail()
                return
            self.hits.append([name, self.beattime])
            match = None
            level = 0
            score = 0
            test = []
            for hit in self.hits:
                test.append([hit[0], hit[1] - lib.math2.round(self.hits[0][1], 1)])
            for sname, song in songs.items():
                this, perfect = song.eval(test)
                if this > level:
                    match = sname
                    level = this
                    score = perfect
            if level == 0:
                lib.sound.play(1, name + "_3", lib.settings.sfxvolume)
                lib.sound.play(2, "ch_" + name + "_3", lib.settings.musicvolume)
                self.fail()
            else:
                if abs(nearest - self.beattime) < 0.05:
                    lib.sound.play(1, name, lib.settings.sfxvolume)
                    lib.sound.play(2, "ch_" + name, lib.settings.musicvolume)
                else:
                    lib.sound.play(1, name + "_2", lib.settings.sfxvolume)
                    lib.sound.play(2, "ch_" + name + "_2", lib.settings.musicvolume)
                for entity in self.entities:
                    if isinstance(entity, lib.pon.generic.Pon):
                        if entity.friendly and not entity.hatapon:
                            entity.animation(name, time = 0.75)
                if level == 2:
                    if score == 1:
                        lib.sound.play(3, "perfect", lib.settings.sfxvolume)
    def update(self):
        if self.paused:
            self.paused = False
            return
        self.time += lib.game.deltatime
        self.beattime = self.time * (self.bpm / 60)

        if self.time >= -0.25:
            if lib.input.getkey("square")[1]:
                self.drum("pata")
            if lib.input.getkey("circle")[1]:
                self.drum("pon")
            if lib.input.getkey("cross")[1]:
                self.drum("don")
            if lib.input.getkey("triangle")[1]:
                self.drum("chaka")
        
        if self.calling:
            if self.combo != -1:
                if self.beattime % 4 >= 0.75:
                    level = 0
                    test = []
                    for hit in self.hits:
                        test.append([hit[0], hit[1] - lib.math2.round(self.hits[0][1], 0.5)])
                    for sname, song in songs.items():
                        this, perfect = song.eval(test, now = self.beattime % 4)
                        if this > level:
                            level = this
                    if level == 0:
                        self.fail()
        if self.beat != math.floor(self.beattime):
            self.beat = math.floor(self.beattime)
            if self.combo == -1:
                match = None
                level = 0
                test = []
                for hit in self.hits:
                    test.append([hit[0], hit[1] - lib.math2.round(self.hits[0][1], 0.5)])
                for sname, song in songs.items():
                    this, perfect = song.eval(test)
                    if this > level:
                        match = sname
                        level = this
                if level == 2:
                    if self.beginnext:
                        self.beginnext = False
                    else:
                        self.combo = 0
                        self.time = 0
                        self.beattime = 0
                        self.beat = 0
                        self.measure = -1
            if self.measure != math.floor(self.beattime / 4):
                self.measure = math.floor(self.beattime / 4)
                if self.time >= 0:
                    if self.combo != -1:
                        if self.calling:
                            match = None
                            level = 0
                            score = 0
                            test = []
                            for hit in self.hits:
                                test.append([hit[0], hit[1] - lib.math2.round(self.hits[0][1], 0.5)])
                            for sname, song in songs.items():
                                this, perfect = song.eval(test)
                                if this > level:
                                    match = sname
                                    level = this
                                    score = perfect
                            if level == 2:
                                self.calling = False
                                self.combo += 1
                                if self.fever < 1:
                                    if (self.combo > 2 and score == 1) or self.combo > 9:
                                        self.fever = 1
                                else:
                                    if score == 1:
                                        self.feverwarn = 0
                                    else:
                                        if self.feverwarn != 4:
                                            self.feverwarn = min(math.ceil(self.feverwarn + (1 - score) * 4), 4)
                                        else:
                                            self.feverwarn = 5
                                    if self.feverwarn == 4:
                                        lib.sound.play(1, "Danger", lib.settings.sfxvolume)
                                    elif self.feverwarn > 4:
                                        self.fever = 0
                                        self.combo = 1
                                        self.feverwarn = 0
                                        lib.sound.play(3, "Fail", lib.settings.musicvolume)
                                if self.fever >= 1:
                                    if self.fevertime % 2 == 1:
                                        lib.sound.play(4, match + "-02", lib.settings.musicvolume)
                                    else:
                                        lib.sound.play(4, match + "-03", lib.settings.musicvolume)
                                elif self.combo >= 5:
                                    lib.sound.play(4, match + "-01", lib.settings.musicvolume)
                                else:
                                    lib.sound.play(4, match + "-00", lib.settings.musicvolume)
                                if match == "March":
                                    self.marker = self.hatapon.x + 200
                                    for entity in self.entities:
                                        if isinstance(entity, lib.pon.generic.Pon):
                                            if entity.friendly:
                                                entity.march(self.marker, 100)
                                elif match == "Attack":
                                    for entity in self.entities:
                                        if isinstance(entity, lib.pon.generic.Pon):
                                            if entity.friendly:
                                                entity.attack()
                                elif match == "Defend":
                                    for entity in self.entities:
                                        if isinstance(entity, lib.pon.generic.Pon):
                                            if entity.friendly:
                                                entity.defend()
                                elif match == "Charge":
                                    for entity in self.entities:
                                        if isinstance(entity, lib.pon.generic.Pon):
                                            if entity.friendly:
                                                entity.charge()
                            else:
                                self.fail()
                            self.hits = []
                        else:
                            self.calling = True
                        if not self.calling:
                            if self.fever < 1:
                                if self.fevertime != 0:
                                    self.fevertime = 0
                                num = str(self.combo)
                                if len(num) == 1:
                                    num = "0" + num
                                lib.sound.play(0, "Combo-" + num, lib.settings.musicvolume)
                            else:
                                if self.fevertime == 0:
                                    self.fevertime = 1
                                else:
                                    self.fevertime += 1
                                    if self.fevertime > 17:
                                        self.fevertime = 2
                                if self.fevertime == 1:
                                    lib.sound.play(4, "Fever", lib.settings.musicvolume)
                                    lib.sound.play(0, "Combo-10", lib.settings.musicvolume)
                                else:
                                    num = str(self.fevertime - 1)
                                    if len(num) == 1:
                                        num = "0" + num
                                    lib.sound.play(0, "Fever-" + num, lib.settings.musicvolume)
                    if self.combo == -1:
                        self.calling = True
                        if self.fevertime != 0:
                            self.fevertime = 0
                            lib.sound.play(4, "Fail", lib.settings.musicvolume)
                        if self.measure == 0:
                            lib.sound.play(0, "Begin-01", lib.settings.musicvolume)
                        elif self.measure % 2 == 0:
                            lib.sound.play(0, "Begin-02", lib.settings.musicvolume)
            if self.time < 0:
                if self.beat == -4:
                    lib.sound.play(0, "Countdown-01", lib.settings.sfxvolume)
                elif self.beat == -3:
                    lib.sound.play(0, "Countdown-02", lib.settings.sfxvolume)
                elif self.beat == -2:
                    lib.sound.play(0, "Countdown-03", lib.settings.sfxvolume)
                elif self.beat == -1:
                    lib.sound.play(0, "Countdown-04", lib.settings.sfxvolume)
            #print(self.measure, self.beat)

        for entity in self.entities:
            entity.timer = self.time
            entity.update()
            if isinstance(entity, lib.pon.generic.Pon):
                if entity.hatapon:
                    self.camerax = lib.math2.lerp(self.camerax, entity.x - 200, lib.game.deltatime * 2)

    def draw(self):
        lib.game.screen.fill((200, 200, 250))

        if self.cameray < 0:
            lib.graphics.rect((10, 10, 10), (0, lib.game.height + self.cameray, lib.game.width, -self.cameray))
        
        for entity in self.entities:
            entity.draw()
        
        lib.graphics.rect((255, 255, 255), (self.marker - self.camerax, lib.game.height + self.cameray, 30, 5))

        for x in range(math.floor(self.camerax / 200) * 200 - 200, math.floor(self.camerax / 200) * 200 + lib.game.width + 200, 200):
            lib.graphics.rect((255, 255, 255), (x - self.camerax - 1, lib.game.height + self.cameray, 2, x % 400 == 0 and 20 or 10))
        
        if self.combo > 1:
            color = (20, 20, 20)
            wormrect = pygame.Rect(0, 50, 400, 200)
            worm = pygame.Surface(wormrect.size, pygame.SRCALPHA)
            for x in range(350):
                y = 0
                if self.fever >= 1:
                    y = 65 - 30 * math.sin((self.beattime * 2 - ((x + 80) / 200)) * math.pi) * max(lib.math2.bias(1 - (x + 80) / 350, 0.1), 0)
                elif self.combo >= 5:
                    y = 65 - 30 * math.sin((self.beattime * 2 + ((x + 80) / 200)) * math.pi) * (1 - max(lib.math2.bias(1 - (x + 80) / 350, 0.5), 0))
                else:
                    s = math.sin(((x + 80) / 150) * math.pi * 3) * abs(math.sin(self.beattime * math.pi)) * max(lib.math2.bias(1 - (x + 80) / 350, 0.01), 0)
                    if s < 0:
                        s = s * 0.5
                    s = s + math.sin((self.beattime * 2 + ((x + 80) / 200)) * math.pi) * (1 - max(lib.math2.bias(1 - (x + 80) / 350, 0.001), 0)) * 1.5
                    y = 65 - 10 * s
                if self.fever >= 1:
                    comboworm_segments_back[x].draw((x, y), dest = worm)
                    comboworm_segments_fever[x].draw((x, y), dest = worm)
                    if self.feverwarn == 4:
                        comboworm_segments_top_alt[x].draw((x, y), dest = worm)
                    else:
                        comboworm_segments_top[x].draw((x, y), dest = worm)
                else:
                    comboworm_segments[x].draw((x, y), dest = worm)
                    if self.combo >= 5:
                        comboworm_segments_top_alt[x].draw((x, y), dest = worm)
                    else:
                        comboworm_segments_top[x].draw((x, y), dest = worm)
            if self.fever >= 1:
                mult = 1 + (1 - self.beattime % 1) * 0.2
                worm = pygame.transform.scale(worm, (math.floor(400 * mult), math.floor(200 * mult)))
                wormrect.y = wormrect.y - 100 * (mult - 1)
            lib.game.screen.blit(worm, wormrect)
            if self.fever < 1:
                mult = 1.1 + math.sin(self.beattime * math.pi * 2) * 0.1
                combotext_numerals[self.combo].draw((30 - 25 * (mult - 1), 150 - 50 * (mult - 1)), size = (math.floor(50 * mult), math.floor(50 * mult)))
                combotext_numerals_top[self.combo].draw((30 - 25 * (mult - 1), 150 - 50 * (mult - 1)), size = (math.floor(50 * mult), math.floor(50 * mult)), alpha = 0.125 + math.sin(self.beattime * math.pi * 2) * 0.125)
                combotext_combo.draw((60, 150))
            else:
                xmult = 1.05 + math.sin((self.beattime - 0.25) * math.pi * 2) * 0.05
                ymult = 1.4 + math.sin(self.beattime * math.pi * 2) * 0.4
                combotext_fever.draw((45 - 100 * (xmult - 1), 160 - 50 * (ymult - 1)), size = (math.floor(200 * xmult), math.floor(50 * ymult)))
        
        if self.calling:
            color = (255, 255, 255)
            transparency = 1 - self.beattime % 1
            if self.fever >= 1:
                frame = math.floor(lib.game.frame / 4)
                if frame % 4 == 1:
                    color = (0, 255, 255)
                elif frame % 4 == 2:
                    color = (0, 255, 0)
                elif frame % 4 == 3:
                    color = (255, 255, 0)
                lib.graphics.rect(color, (14, 16, lib.game.width - 28, 8), transparency)
                lib.graphics.rect(color, (14, 24, 8, lib.game.height - 46), transparency)
                lib.graphics.rect(color, (14, lib.game.height - 22, lib.game.width - 28, 8), transparency)
                lib.graphics.rect(color, (lib.game.width - 22, 24, 8, lib.game.height - 46), transparency)
            else:
                lib.graphics.rect(color, (16, 16, lib.game.width - 32, 4), transparency)
                lib.graphics.rect(color, (16, 20, 4, lib.game.height - 40), transparency)
                lib.graphics.rect(color, (16, lib.game.height - 20, lib.game.width - 32, 4), transparency)
                lib.graphics.rect(color, (lib.game.width - 20, 20, 4, lib.game.height - 40), transparency)
        else:
            color = (50, 50, 50)
            transparency = 1 - self.beattime % 1
            if self.beat % 4 == 3:
                frame = math.floor(lib.game.frame / 4)
                if frame % 2 == 0:
                    color = (255, 255, 255)
            lib.graphics.rect(color, (14, 14, lib.game.width - 28, 2), transparency)
            lib.graphics.rect(color, (14, 16, 2, lib.game.height - 32), transparency)
            lib.graphics.rect(color, (14, lib.game.height - 16, lib.game.width - 28, 2), transparency)
            lib.graphics.rect(color, (lib.game.width - 16, 16, 2, lib.game.height - 32), transparency)
            lib.graphics.rect(color, (20, 20, lib.game.width - 40, 2), transparency)
            lib.graphics.rect(color, (20, 22, 2, lib.game.height - 44), transparency)
            lib.graphics.rect(color, (20, lib.game.height - 22, lib.game.width - 40, 2), transparency)
            lib.graphics.rect(color, (lib.game.width - 22, 22, 2, lib.game.height - 44), transparency)
