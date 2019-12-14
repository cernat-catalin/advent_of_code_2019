from itertools import combinations
import re
import numpy as np
from math import gcd


def simulate_one_step(velocities, positions):
    for (i, j) in combinations(range(4), 2):
        upd = np.sign(positions[j] - positions[i])
        velocities[i] += upd
        velocities[j] -= upd
    positions += velocities

    return velocities, positions


def simulate(velocities, positions, n=1, infinite=False):
    velocities = np.copy(velocities)
    positions  = np.copy(positions)
    period     = 1

    if not infinite:
        for _ in range(n):
            velocities, positions = simulate_one_step(velocities, positions)
    else:
        initial_velocities = np.copy(velocities)
        initial_positions = np.copy(positions)

        velocities, positions = simulate_one_step(velocities, positions)
        while not np.all(initial_positions == positions) and not np.all(initial_velocities == velocities):
            velocities, positions = simulate_one_step(velocities, positions)
            period += 1

    return velocities, positions, period


def calculate_energy(velocities, positions):
    return sum(sum(abs(velocities[i])) * sum(abs(positions[i])) for i in range(4))


with open('day12/input') as f:
    positions = np.array([[int(x) for x in re.findall(r'[-\d]+', line.rstrip())] for line in f.readlines()], dtype=int)
    velocities = np.zeros(positions.shape, dtype=int)

    velocities_, positions_, _ = simulate(velocities, positions, n=1000)
    print(calculate_energy(velocities_, positions_)) # part one

    lcm = lambda x, y: (x * y) // gcd(x, y)
    _, _, period_x = simulate(velocities[:, 0], positions[:, 0], infinite=True)
    _, _, period_y = simulate(velocities[:, 1], positions[:, 1], infinite=True)
    _, _, period_z = simulate(velocities[:, 2], positions[:, 2], infinite=True)

    print(period_x, period_y, period_z)

    print(lcm(lcm(period_x, period_y), period_z) * 2) # part two