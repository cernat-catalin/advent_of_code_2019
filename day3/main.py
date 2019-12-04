import numpy as np


def move(position, instruction):
    dir_  = instruction[0]
    value = int(instruction[1:])

    if   dir_ == 'R': return position + (value, 0), value
    elif dir_ == 'D': return position + (0, -value), value
    elif dir_ == 'L': return position + (-value, 0), value
    elif dir_ == 'U': return position + (0, value), value
    

def construct_lines(position, instructions, delay):
    if instructions == []:
        return []
    else:
        new_position, moved = move(position, instructions[0])
        lines = construct_lines(new_position, instructions[1:], delay + moved)
        lines.append((position, new_position, delay))
        return lines


def lines_intersection(line1, line2):
    (p1, p2, _) = line1
    (p3, p4, _) = line2

    if (p1[0] == p2[0] and p3[1] == p4[1]
            and ((p3[0] <= p1[0] and p1[0] <= p4[0]) or (p4[0] <= p1[0] and p1[0] <= p3[0]))
            and ((p1[1] <= p3[1] and p3[1] <= p2[1]) or (p2[1] <= p3[1] and p3[1] <= p1[1]))):
        return True, (p1[0], p3[1])
    elif (p1[1] == p2[1] and p3[0] == p4[0]
            and ((p1[0] <= p3[0] and p3[0] <= p2[0]) or (p2[0] <= p3[0] and p3[0] <= p1[0]))
            and ((p3[1] <= p1[1] and p1[1] <= p4[1]) or (p4[1] <= p1[1] and p1[1] <= p3[1]))):
        return True, (p3[0], p1[1])
    else:
        return False, None


def find_all_intersections(lines1, lines2):
    intersections = []
    for line1 in lines1:
        for line2 in lines2:
            did_intersect, point = lines_intersection(line1, line2)
            if did_intersect and point != (0, 0):
                intersections.append((line1, line2, point))
    return intersections


def compute_delay(intersection):
    (p1, p2, delay1), (p3, p4, delay2), (x, y) = intersection
    if p1[0] == p2[0]:
        return (delay1 + abs(y - p1[1]) + delay2 + abs(x - p3[0]))
    else:
        return (delay1 + abs(x - p1[0]) + delay2 + abs(y - p3[1]))


with open('day3/input') as f:
    instructions = [line.split(',') for line in f.readlines()]

    lines1 = construct_lines(np.array([0, 0]), instructions[0], 0)
    lines2 = construct_lines(np.array([0, 0]), instructions[1], 0)
    intersections = find_all_intersections(lines1, lines2)

    # part one
    print(min([abs(x) + abs(y) for (line1, line2, (x, y)) in intersections]))

    # part two
    print(min([compute_delay(intersection) for intersection in intersections]))

