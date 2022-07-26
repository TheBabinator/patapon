import lib.pon.statuseffect

content = {
    "burn": lib.pon.statuseffect.StatusEffect("burn", {
        "damageMin": 1,
        "damageMax": 5,
        "damageTime": 0.6,
        "critChance": 0.05,
        "critMult": 3,
        "particle": 1,
    }),
}
