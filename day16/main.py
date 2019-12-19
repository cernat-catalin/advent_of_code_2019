from typing import List
from itertools import count, repeat
from functools import reduce

def print_n_pattern(n, pattern):
    for _ in range(n):
        print(next(pattern), end=' ')
    print('')


def step(digits: List[int], base_pattern: List[int], n: int) -> List[int]:
    for _ in range(n):
        new_digits = []
        for i in range(len(digits)):
            pattern = (base_pattern[(j // (i + 1)) % 4] for j in count())
            next(pattern)

            new_digit = sum(( next(pattern) * digit for digit in digits ))
            new_digits.append(abs(new_digit) % 10)

        digits = new_digits
    
    return digits

def step_2(digits: List[int], n: int) -> List[int]:

    for _ in range(n):
        new_digits = []
        s = sum(digits)
        for i in range(len(digits)):
            new_digits.append(s % 10)
            s -= digits[i]
        digits = new_digits
    
    return digits

with open('day16/input') as f:
    digits = [int(x) for x in f.readline().strip()]
    base_pattern = [0, 1, 0, -1]

    # part one
    new_digits = step(digits[:], base_pattern, 1)
    print(''.join((str(x) for x in new_digits[:8])))

    # part two
    offset = reduce(lambda x, y: x * 10 + y,  digits[:7])
    digits = (digits * 10000)[offset:]
    new_digits = step_2(digits, 100)
    print(''.join((str(x) for x in new_digits[:8])))
