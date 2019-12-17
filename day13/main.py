import sys, os
sys.path.append(os.getcwd())

from lib.intcode import Intcode, ReturnCode, run, create_intcode
import numpy as np
from typing import NamedTuple


class GameSate(NamedTuple):
    score: int
    paddle_pos: tuple
    ball_pos: tuple


def update_game_state(game_state, output_stream):
    score = game_state.score
    paddle_pos = game_state.paddle_pos
    ball_pos = game_state.ball_pos

    while len(output_stream) >= 3:
        (x, y, t) = output_stream[:3]
        del output_stream[:3]

        if x == -1 and y == 0:
            score = t
        elif t == 3:
            paddle_pos = (x, y)
        elif t == 4:
            ball_pos = (x, y)

    return GameSate(score, paddle_pos, ball_pos)


def joystick_direction(game_state):
    if game_state.paddle_pos[0] < game_state.ball_pos[0]:
        return 1
    elif game_state.paddle_pos[0] > game_state.ball_pos[0]:
        return -1
    else:
        return 0


with open('day13/input') as f:
    program = [int(x) for x in f.readline().rstrip().split(',')]

    output_stream = []
    intcode = run(create_intcode(program, [], output_stream))

    output = np.array(output_stream)
    print(np.sum(output[2::3] == 2)) # part one

    program[0] = 2
    output_stream = []
    input_stream = []
    intcode = run(create_intcode(program, input_stream, output_stream))

    code = ReturnCode.NOT_STATED
    game_state = GameSate(0, (0, 0), (0, 0))

    while code != ReturnCode.EXIT_SUCCESS:
        intcode = run(intcode)
        code = intcode.return_code

        game_state = update_game_state(game_state, output_stream)

        direction = joystick_direction(game_state)
        input_stream.append(direction)

    print(game_state.score)