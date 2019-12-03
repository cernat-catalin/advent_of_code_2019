def fuel_for_mass(m):
    f = m // 3 - 2
    return f + fuel_for_mass(f) if f > 0 else 0

with open('input') as f:
    ms = [int(line) for line in f.readlines()]
    result = sum([fuel_for_mass(m) for m in ms])
    print(result)
