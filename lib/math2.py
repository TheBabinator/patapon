import math

def lerp(a, b, alpha):
    return a + (b - a) * alpha

def lerptup(tuplea, tupleb, alpha):
    out = []
    i = -1
    for a in tuplea:
        i += 1
        b = tupleb[i]
        out.append(lerp(a, b, alpha))
    return tuple(out)

def bias(x, bias):
    return (bias ** x - 1) / (bias - 1)

def round(x, unit):
    mod = x % unit
    floor = math.floor(x / unit)
    if mod >= unit / 2:
        return (floor + 1) * unit
    return floor * unit
