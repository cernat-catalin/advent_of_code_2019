import re
from typing import NamedTuple, List, Tuple


class Reaction(NamedTuple):
    left: List[Tuple[int, str]]
    right: Tuple[int, str]


def create_reaction(unparsed_reaction: List[str]) -> Reaction:
    parse_element = lambda x: (int(x.split(' ')[0]), x.split(' ')[1])
    left = [parse_element(element) for element in unparsed_reaction[:-1]]
    right = parse_element(unparsed_reaction[-1])
    return Reaction(left, right)


with open ('day14/input') as f:
    reactions = [re.findall(r'[\d]+ [\w]+', line) for line in f.readlines()]
    reactions = [create_reaction(reaction) for reaction in reactions]
    print(reactions[0])