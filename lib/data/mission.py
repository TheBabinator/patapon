def expand(string):
    out = string.split(" ")
    for x in range(len(out)):
        out[x] = int(out[x])
    return tuple(out)

class Mission:
    def __init__(self, name):
        file = open("assets/missions/" + name + ".pata", "r")
        lines = file.read().split("\n")
        file.close()

        self.name = lines[0]
        self.lore = lines[1]
        self.track = lines[2]
        self.sky = expand(lines[3])
        self.ground = expand(lines[4])
