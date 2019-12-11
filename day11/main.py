from typing import NamedTuple
from enum import Enum

import numpy as np


class ReturnCode(Enum):
    EXIT_SUCCESS = 0
    NOT_STATED = 1
    RUNNING = 2
    WAITING_ON_INPUT = 3
    ERROR = 4


class Parameter(NamedTuple):
    mode: int
    value: int


class Intcode(NamedTuple):
    memory: list
    program_counter: int
    relative_base_offset: int
    intput_stream: list
    output_stream: list
    return_code: ReturnCode


def read_instruction(intcode: Intcode):
    memory = intcode.memory
    pc     = intcode.program_counter

    get_param = lambda addr: memory[addr] if (len(memory) > addr) else None

    opcode = memory[pc] % 100
    mode_0 = (memory[pc] // 100) % 10
    mode_1 = (memory[pc] // 1000) % 10
    mode_2 = (memory[pc] // 10000) % 10

    return opcode, [Parameter(mode_0, get_param(pc + 1)), Parameter(mode_1, get_param(pc + 2)), Parameter(mode_2, get_param(pc + 3))]


def run_once(intcode: Intcode):
    memory = intcode.memory
    pc = intcode.program_counter
    rbo = intcode.relative_base_offset
    input_stream = intcode.intput_stream
    output_stream = intcode.output_stream
    return_code = ReturnCode.RUNNING
    
    read_addr  = lambda param: param.value if param.mode == 0 else rbo + param.value
    read_value = lambda param: param.value if param.mode == 1 else memory[read_addr(param)]
    opcode, p = read_instruction(intcode)

    if opcode == 1:
        memory[read_addr(p[2])] = read_value(p[0]) + read_value(p[1])
        pc += 4
    elif opcode == 2:
        memory[read_addr(p[2])] = read_value(p[0]) * read_value(p[1])
        pc += 4
    elif opcode == 3:
        if len(input_stream) > 0:
            memory[read_addr(p[0])] = input_stream[0]
            input_stream.pop(0)
            pc += 2
        else:
            return_code = ReturnCode.WAITING_ON_INPUT
    elif opcode == 4:
        output_stream.append(read_value(p[0]))
        pc += 2
    elif opcode == 5:
        pc = read_value(p[1]) if read_value(p[0]) != 0 else pc + 3
    elif opcode == 6:
        pc = read_value(p[1]) if read_value(p[0]) == 0 else pc + 3
    elif opcode == 7:
        memory[read_addr(p[2])] = 1 if read_value(p[0]) < read_value(p[1]) else 0
        pc += 4
    elif opcode == 8:
        memory[read_addr(p[2])] = 1 if read_value(p[0]) == read_value(p[1]) else 0
        pc += 4
    elif opcode == 9:
        rbo += read_value(p[0])
        pc += 2
    elif opcode == 99:
        return_code = ReturnCode.EXIT_SUCCESS
    else:
        return_code = ReturnCode.ERROR

    return Intcode(memory, pc, rbo, input_stream, output_stream, return_code)


def run(intcode: Intcode):
    intcode = run_once(intcode)
    while intcode.return_code == ReturnCode.RUNNING:
        intcode = run_once(intcode)
    return intcode


def create_intcode(program, input_stream, output_stream):
    memory = program[:] + [0 for i in range(1000)] # extend by 1k elements
    return Intcode(memory, 0, 0, input_stream, output_stream, ReturnCode.NOT_STATED)


with open('day11/input') as f:
    x = [int(i) for i in f.readline().split(',')]

    n       = 100
    panel   = np.zeros((n, n), dtype=int)
    painted = np.zeros((n, n), dtype=bool)

    position      = (n // 2, n // 2)
    directions    = [(-1, 0), (0, -1), (1, 0), (0, 1)]
    direction_idx = 0

    turn_left_90  = lambda idx: (idx + 1) % 4
    turn_right_90 = lambda idx: (idx + 3) % 4

    input_stream  = []
    output_stream = []
    intcode       = create_intcode(x, input_stream, output_stream)

    panel[position] = 1 # comment this for part one answer
    while intcode.return_code != ReturnCode.EXIT_SUCCESS:
        input_stream.append(panel[position])
        intcode = run(intcode)

        color, turn = intcode.output_stream
        intcode.output_stream.clear()

        panel[position] = color
        painted[position] = True

        direction_idx = turn_left_90(direction_idx) if turn == 0 else turn_right_90(direction_idx)
        position = (position[0] + directions[direction_idx][0], position[1] + directions[direction_idx][1])

    # print(np.sum(painted)) # part one

    message = '\n'.join((''.join(str(x) for x in row) for row in panel)).replace('0', ' ')
    print(message)