from collections import defaultdict
import numpy as np
from fractions import Fraction
from itertools import zip_longest
from sortedcontainers import SortedSet, SortedDict


def num_detections(belt, n, m, x, y):
    INF = 1e12
    slopes_1 = defaultdict(list)
    slopes_2 = defaultdict(list)

    for i in range(0, n):
        for j in range(0, m):
            if belt[i][j] and not (x == i and y == j):
                a, b = x - i, y - j

                if b == 0:
                    slopes_1[Fraction(INF * -np.sign(a))].append((i, j))
                else:
                    c = Fraction(a, b)
                    if b < 0:
                        slopes_1[c].append((i, j))
                    else:
                        slopes_2[c].append((i, j))

    return (x, y), slopes_1, slopes_2


with open('day10/input') as f:
    belt = [[1 if y == '#' else 0 for y in line.rstrip()]
            for line in f.readlines()]
    n, m = len(belt), len(belt[0])

    (x, y), slopes_1, slopes_2 = max((num_detections(belt, n, m, i, j) for i in range(0, n)
                                      for j in range(0, m) if belt[i][j] == 1), key=lambda x: len(x[1]) + len(x[2]))

    print(len(slopes_1) + len(slopes_2))  # part one

    combined_angles = [sorted(slope_class, key=lambda p: abs(p[0] - x) + abs(p[1] - y))
                       for slope_class in map(lambda x: x[1], sorted(slopes_1.items()) + sorted(slopes_2.items()))]
    combined_angles = list(map(list, zip_longest(*combined_angles)))
    combined_angles = np.array(combined_angles).flatten()
    combined_angles = combined_angles[combined_angles != None]

    (b, a) = combined_angles[199]
    print(a * 100 + b)
