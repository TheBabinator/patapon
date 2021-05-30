import os
import math
import random
import lib.game
import lib.input
import lib.math2
import lib.graphics
import lib.sound
import lib.entity
import lib.pon.generic
import lib.settings

songs = {}

class Song:
    def __init__(self, name, pattern):
        self.name = name
        self.pattern = pattern
        songs[self.name] = self
    
    def eval(self, match, now = 0):
        if len(match) > len(self.pattern):
            return 0
        i = -1
        for hit in match:
            i += 1
            if hit[0] != self.pattern[i][0]:
                return 0
            if abs(hit[1] - self.pattern[i][1]) > 0.2:
                return 0
        if len(match) != len(self.pattern):
            if now > self.pattern[i + 1][1] + 0.25:
                return 0
            return 1
        return 2

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

        self.bpm = 120
        self.time = -2.5
        self.beattime = 0
        self.beat = 0
        self.measure = 0
        self.calling = False
        self.combo = -1
        self.combotime = 0
        self.fever = 0
        self.fevertime = 0
        self.hits = []
        self.begin = False

        pon = lib.pon.generic.Pon(self, True)
        pon.x = 0
        self.entities.append(pon)

        pon = lib.pon.generic.Pon(self, True)
        pon.x = 50
        self.entities.append(pon)

        pon = lib.pon.generic.Pon(self, True)
        pon.x = 100
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
        self.time = 0
        self.beattime = 0
        self.beat = -1
        self.measure = -1
        lib.sound.play(2, "Complain-0" + str(random.randint(1, 2)), lib.settings.sfxvolume)

    def drum(self, name):
        nearest = lib.math2.round(self.beattime, 0.5)
        if self.combo == -1:
            self.hits.append([name, self.beattime])
            if len(self.hits) > 4:
                self.hits.pop(0)
            match = None
            level = 0
            while len(self.hits) > 0:
                test = []
                for hit in self.hits:
                    test.append([hit[0], hit[1] - lib.math2.round(self.hits[0][1], 1)])
                for sname, song in songs.items():
                    this = song.eval(test)
                    if this > level:
                        match = sname
                        level = this
                if match:
                    break
                else:
                    self.hits.pop(0)
            if level == 0:
                lib.sound.play(1, name + "_3", lib.settings.sfxvolume)
            else:
                if abs(nearest - self.beattime) < 0.05:
                    lib.sound.play(1, name, lib.settings.sfxvolume)
                else:
                    lib.sound.play(1, name + "_2", lib.settings.sfxvolume)
                if level == 2:
                    lib.sound.play(3, "perfect", lib.settings.sfxvolume)
                    self.begin = True
        else:
            if lib.math2.round(self.beattime, 0.5) % 8 < 4:
                self.fail()
                return
            self.hits.append([name, self.beattime])
            if len(self.hits) > 4:
                self.fail()
                return
            match = None
            level = 0
            test = []
            for hit in self.hits:
                test.append([hit[0], hit[1] - lib.math2.round(self.hits[0][1], 1)])
            for sname, song in songs.items():
                this = song.eval(test)
                if this > level:
                    match = sname
                    level = this
            if level == 0:
                lib.sound.play(1, name + "_3", lib.settings.sfxvolume)
                self.fail()
            else:
                if abs(nearest - self.beattime) < 0.05:
                    lib.sound.play(1, name, lib.settings.sfxvolume)
                else:
                    lib.sound.play(1, name + "_2", lib.settings.sfxvolume)
                if level == 2:
                    lib.sound.play(3, "perfect", lib.settings.sfxvolume)

    def update(self):
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

        if self.beat != math.floor(self.beattime):
            self.beat = math.floor(self.beattime)
            if self.combo == -1:
                match = None
                level = 0
                test = []
                for hit in self.hits:
                    test.append([hit[0], hit[1] - lib.math2.round(self.hits[0][1], 0.5)])
                for sname, song in songs.items():
                    this = song.eval(test)
                    if this > level:
                        match = sname
                        level = this
                if level == 2:
                    if self.begin:
                        self.begin = False
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
                            test = []
                            for hit in self.hits:
                                test.append([hit[0], hit[1] - lib.math2.round(self.hits[0][1], 0.5)])
                            for sname, song in songs.items():
                                this = song.eval(test)
                                if this > level:
                                    match = sname
                                    level = this
                            if level == 2:
                                self.calling = False
                                self.combo += 1
                                progression = 0.2
                                self.fever = min(max(self.fever + progression, 0), 2)
                                if self.fever >= 1:
                                    if self.fevertime % 2 == 1:
                                        lib.sound.play(2, match + "-02", lib.settings.musicvolume)
                                    else:
                                        lib.sound.play(2, match + "-03", lib.settings.musicvolume)
                                elif self.fever >= 0.5:
                                    lib.sound.play(2, match + "-01", lib.settings.musicvolume)
                                else:
                                    lib.sound.play(2, match + "-00", lib.settings.musicvolume)
                            else:
                                self.fail()
                            self.hits = []
                        else:
                            self.calling = True
                        if not self.calling:
                            if self.fever < 1:
                                if self.fevertime != 0:
                                    self.fevertime = 0
                                if self.combotime == 0:
                                    self.combotime = 1
                                else:
                                    self.combotime += 1
                                    if self.combotime > 9:
                                        self.combotime = 1
                                num = str(self.combotime)
                                if len(num) == 1:
                                    num = "0" + num
                                lib.sound.play(0, "Combo-" + num, lib.settings.musicvolume)
                            else:
                                if self.combotime != 0:
                                    self.combotime = 0
                                    lib.sound.play(2, "Fever", lib.settings.musicvolume)
                                if self.fevertime == 0:
                                    self.fevertime = 1
                                else:
                                    self.fevertime += 1
                                    if self.fevertime > 17:
                                        self.fevertime = 2
                                if self.fevertime == 1:
                                    lib.sound.play(0, "Combo-10", lib.settings.musicvolume)
                                else:
                                    num = str(self.fevertime - 1)
                                    if len(num) == 1:
                                        num = "0" + num
                                    lib.sound.play(0, "Fever-" + num, lib.settings.musicvolume)
                    if self.combo == -1:
                        self.calling = True
                        if self.combotime != 0:
                            self.combotime = 0
                        if self.fevertime != 0:
                            self.fevertime = 0
                            lib.sound.play(2, "Fail", lib.settings.musicvolume)
                        if self.measure == 0:
                            lib.sound.play(0, "Begin-01", lib.settings.musicvolume)
                        elif self.measure % 2 == 0:
                            lib.sound.play(0, "Begin-02", lib.settings.musicvolume)
            if self.time < 0:
                if self.beat == -4:
                    lib.sound.play(2, "Countdown-01", lib.settings.sfxvolume)
                elif self.beat == -3:
                    lib.sound.play(2, "Countdown-02", lib.settings.sfxvolume)
                elif self.beat == -2:
                    lib.sound.play(2, "Countdown-03", lib.settings.sfxvolume)
                elif self.beat == -1:
                    lib.sound.play(2, "Countdown-04", lib.settings.sfxvolume)
            #print(self.measure, self.beat)

        for entity in self.entities:
            entity.timer = self.time
            entity.update()

    def draw(self):
        lib.game.screen.fill((200, 200, 250))

        if self.cameray < 0:
            lib.graphics.rect((10, 10, 10), (0, lib.game.height + self.cameray, lib.game.width, -self.cameray))
        
        for entity in self.entities:
            entity.draw()
        
        if self.combo > 1:
            color = (20, 20, 20)
            if self.fever >= 1:
                color = (200, 0, 0)
                color2 = lib.math2.lerptup((255, 200, 50), (255, 50, 0), self.beattime % 1)
                for x in range(300):
                    if x / 300 >= self.fever - 1:
                        lib.graphics.rect(color, (x, 150 - 30 * math.sin((self.beattime * 2 - (x / 200)) * math.pi) * lib.math2.bias(1 - x / 300, 0.1), 1, 50))
                    else:
                        lib.graphics.rect(color2, (x, 150 - 30 * math.sin((self.beattime * 2 - (x / 200)) * math.pi) * lib.math2.bias(1 - x / 300, 0.1), 1, 50))
            elif self.fever >= 0.5:
                for x in range(300):
                    lib.graphics.rect(color, (x, 150 - 20 * math.sin((self.beattime * 2 + (x / 200)) * math.pi), 1, 50))
            else:
                for x in range(300):
                    lib.graphics.rect(color, (x, 150 - 20 * abs(math.sin((self.beattime + (x / 150)) * math.pi)), 1, 50))

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
