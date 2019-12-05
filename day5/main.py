import numpy as np


def process(x, pc, ins, outs):
    load = lambda mode, val: val if mode == 1 else x[val]

    opcode = x[pc] % 100
    mode_1 = (x[pc] // 100) % 10
    mode_2 = x[pc] // 1000

    if opcode == 1:
        x[x[pc + 3]] = load(mode_1, x[pc + 1]) + load(mode_2, x[pc + 2])
        pc += 4
    elif opcode == 2:
        x[x[pc + 3]] = load(mode_1, x[pc + 1]) * load(mode_2, x[pc + 2])
        pc += 4
    elif opcode == 3:
        x[x[pc + 1]] = ins[0]
        ins = ins[1:]
        pc += 2
    elif opcode == 4:
        outs.append(load(mode_1, x[pc + 1]))
        pc += 2
    elif opcode == 5:
        pc = load(mode_2, x[pc + 2]) if load(mode_1, x[pc + 1]) != 0 else pc + 3
    elif opcode == 6:
        pc = load(mode_2, x[pc + 2]) if load(mode_1, x[pc + 1]) == 0 else pc + 3
    elif opcode == 7:
        x[x[pc + 3]] = 1 if load(mode_1, x[pc + 1]) < load(mode_2, x[pc + 2]) else 0
        pc += 4
    elif opcode == 8:
        x[x[pc + 3]] = 1 if load(mode_1, x[pc + 1]) == load(mode_2, x[pc + 2]) else 0
        pc += 4
    elif x[pc] == 99:
        return outs
    else:
        return None # error

    return process(x, pc, ins, outs)


with open('day5/input') as f:
    x = [int(i) for i in f.readline().split(',')]
    # print(process(x, 0, [1], [])[-1:]) # part one
    print(process(x, 0, [5], [])) # part two