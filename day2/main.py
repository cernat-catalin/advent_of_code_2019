import numpy as np


def process(x, i):
    if x[i] == 1:
        x[x[i + 3]] = x[x[i + 1]] + x[x[i + 2]]
    elif x[i] == 2:
        x[x[i + 3]] = x[x[i + 1]] * x[x[i + 2]]
    elif x[i] == 99:
        return x
    else:
        return [-1]
    return process(x, i + 4)


def run_program(x, noun, verb):
    y = x.copy()
    y[1] = noun
    y[2] = verb
    return process(y, 0)[0]


def find_combination(x, target):
    a = np.array([[run_program(x, noun, verb) == target
        for verb in range(100)]
        for noun in range(100)])
    return np.unravel_index(np.argmax(a), a.shape)


with open('input') as f:
    x = [int(i) for i in f.readline().split(',')]
    print(run_program(x, 12, 2)) # part one
    (noun, verb) = find_combination(x, 19690720) # part two
    print(100 * noun + verb)

