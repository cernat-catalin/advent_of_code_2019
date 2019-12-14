from typing import NamedTuple
from enum import Enum
import numpy as np

import sys
from lib.intcode import Intcode, create_intcode, ReturnCode, run


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