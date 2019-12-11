from typing import NamedTuple
from enum import Enum
import itertools


class ReturnCode(Enum):
    EXIT_SUCCESS = 0
    NOT_STATED = 1
    RUNNING = 2
    WAITING_ON_INPUT = 3
    ERROR = 4


class Intcode(NamedTuple):
    memory: list
    program_counter: int
    intput_stream: list
    output_stream: list
    return_code: ReturnCode


def read_instruction(intcode: Intcode):
    memory = intcode.memory
    pc     = intcode.program_counter

    get_param = lambda addr: memory[addr] if (len(memory) > addr) else None

    opcode = memory[pc] % 100
    mode_0 = (memory[pc] // 100) % 10
    mode_1 = memory[pc] // 1000

    return opcode, mode_0, mode_1, [get_param(pc + 1), get_param(pc + 2), get_param(pc + 3)]


def run_once(intcode: Intcode):
    pc = intcode.program_counter
    memory = intcode.memory
    input_stream = intcode.intput_stream
    output_stream = intcode.output_stream
    return_code = ReturnCode.RUNNING
    
    load = lambda mode, value: value if mode == 1 else memory[value]
    opcode, mode_0, mode_1, p = read_instruction(intcode)

    if opcode == 1:
        memory[p[2]] = load(mode_0, p[0]) + load(mode_1, p[1])
        pc += 4
    elif opcode == 2:
        memory[p[2]] = load(mode_0, p[0]) * load(mode_1, p[1])
        pc += 4
    elif opcode == 3:
        if len(input_stream) > 0:
            memory[p[0]] = input_stream[0]
            input_stream.pop(0)
            pc += 2
        else:
            return_code = ReturnCode.WAITING_ON_INPUT
    elif opcode == 4:
        output_stream.append(load(mode_0, p[0]))
        pc += 2
    elif opcode == 5:
        pc = load(mode_1, p[1]) if load(mode_0, p[0]) != 0 else pc + 3
    elif opcode == 6:
        pc = load(mode_1, p[1]) if load(mode_0, p[0]) == 0 else pc + 3
    elif opcode == 7:
        memory[p[2]] = 1 if load(mode_0, p[0]) < load(mode_1, p[1]) else 0
        pc += 4
    elif opcode == 8:
        memory[p[2]] = 1 if load(mode_0, p[0]) == load(mode_1, p[1]) else 0
        pc += 4
    elif opcode == 99:
        return_code = ReturnCode.EXIT_SUCCESS
    else:
        return_code = ReturnCode.ERROR

    return Intcode(memory, pc, input_stream, output_stream, return_code)


def run(intcode: Intcode):
    intcode = run_once(intcode)
    while intcode.return_code == ReturnCode.RUNNING:
        intcode = run_once(intcode)
    return intcode
    

def thruster_signal(program, phases):
    signal = 0
    for phase in phases:
        intcode = Intcode(program[:], 0, [phase, signal], [], ReturnCode.NOT_STATED)
        intcode = run(intcode)
        assert intcode.return_code == ReturnCode.EXIT_SUCCESS
        signal = intcode.output_stream[0]
    return signal


def thruster_signal_loop(program, phases):
    streams = [[phase] for phase in phases]
    streams[0].append(0)

    n = len(phases)
    intcodes = [Intcode(program, 0, streams[i], streams[(i + 1) % 5], ReturnCode.NOT_STATED) for i in range(n)]

    intcodes = [run(intcode) for intcode in intcodes]
    while not all((intcode.return_code == ReturnCode.EXIT_SUCCESS for intcode in intcodes)):
        intcodes = [run(intcode) for intcode in intcodes]

    return streams[0][0]


with open('day7/input') as f:
    x = [int(i) for i in f.readline().split(',')]

    print(max([thruster_signal(x, phases) for phases in list(itertools.permutations([0, 1, 2, 3, 4]))])) # part_one
    print(max([thruster_signal_loop(x, phases) for phases in list(itertools.permutations([5, 6, 7, 8, 9]))])) # part_two 