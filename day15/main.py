import sys, os
sys.path.append(os.getcwd())

from typing import Tuple, List
import numpy as np
from collections import deque

from lib.intcode import Intcode, ReturnCode, run, create_intcode


def move_droid(intcode: Intcode, code: int) -> int:
    intcode.intput_stream.append(code)
    run(intcode)
    return intcode.output_stream.pop()


def dfs_explore(pos: Tuple[int, int], grid: np.array, cell_type: int, intcode: Intcode):
    (x, y) = pos
    directions = [(-1, 0, (1, 2)), (1, 0, (2, 1)), (0, 1, (3, 4)), (0, -1, (4, 3))]

    grid[x][y] = cell_type

    for direction in directions:
        (dx, dy, (code, reverse_code)) = direction
        if grid[x + dx][y + dy] == -1:
            status = move_droid(intcode, code)
            if status == 0:
                grid[x + dx][y + dy] = 0
            else:
                dfs_explore((x + dx, y + dy), grid, status, intcode)
                move_droid(intcode, reverse_code)
    
    return


def distances_bfs(pos: Tuple[int, int], grid: np.array) -> int:
    q = deque()
    directions = [(-1, 0), (1, 0), (0, 1), (0, -1)]
    distances = np.zeros(grid.shape, dtype=int)

    q.append(pos)
    while len(q) > 0:
        (x, y) = q.popleft()
        for direction in directions:
            (dx, dy) = direction
            if grid[x + dx][y + dy] != 0 and distances[x + dx][y + dy] == 0:
                distances[x + dx][y + dy] = distances[x][y] + 1
                q.append((x + dx, y + dy))

    return distances


with open('day15/input') as f:
    program = [int(x) for x in f.readline().rstrip().split(',')]

    n = 10000
    starting_position = (n // 2, n // 2)
    grid = np.ones((n, n), dtype=int) * -1
    intcode = create_intcode(program, [], [])

    dfs_explore(starting_position, grid, 1, intcode)

    oxygen_tank_position = np.argwhere(grid == 2)[0]
    distances = distances_bfs(starting_position, grid)
    print(distances[oxygen_tank_position[0]][oxygen_tank_position[1]]) # part one

    distances = distances_bfs(oxygen_tank_position, grid)
    print(np.max(distances)) # part two
